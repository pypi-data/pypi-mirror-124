#
# Copyright 2018-2021 Elyra Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from abc import ABC
from abc import abstractmethod
import copy
import io
import json
import os
import re
from typing import Dict
from typing import List
from typing import Optional

from entrypoints import get_group_all
from jsonschema import draft7_format_checker
from jsonschema import validate
from jsonschema import ValidationError
from traitlets.config import LoggingConfigurable
from traitlets.config import SingletonConfigurable
from traitlets import Type  # noqa H306

from elyra.metadata.error import SchemaNotFoundError

METADATA_TEST_SCHEMASPACE_ID = "8182fc28-899a-4521-8342-1a0e218c3a4d"
METADATA_TEST_SCHEMASPACE = "metadata-tests"  # exposed via METADATA_TESTING env


class SchemaManager(SingletonConfigurable):
    """Singleton used to store all schemas for all metadata types.
       Note: we currently don't refresh these entries.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # The following exposes the metadata-test schemaspace if true or 1.
        # Metadata testing will enable this env.  Note: this cannot be globally
        # defined, else the file could be loaded before the tests have enable the env.
        self.metadata_testing_enabled = bool(os.getenv("METADATA_TESTING", 0))

        self._meta_schema: dict
        schema_file = os.path.join(os.path.dirname(__file__), 'schemas', 'meta-schema.json')
        with io.open(schema_file, 'r', encoding='utf-8') as f:
            self._meta_schema = json.load(f)
        self._load_schemaspace_schemas()

    def get_schemaspace_names(self) -> list:
        """Returns list of registered schemaspace names."""
        return list(self.schemaspace_id_to_name.values())

    def get_schemaspace_name(self, schemaspace_name_or_id: str) -> str:
        """Returns the human-readable name of the given schemaspace name or id.

        Note that the value returned is the case-sensitive form as stored on
        the Schemaspace instance itself.
        """
        self._validate_schemaspace(schemaspace_name_or_id)
        return self.schemaspaces.get(schemaspace_name_or_id.lower()).name

    def get_schemaspace_schemas(self, schemaspace_name_or_id: str) -> dict:
        self._validate_schemaspace(schemaspace_name_or_id)
        schemaspace = self.schemaspaces.get(schemaspace_name_or_id.lower())
        schemas = schemaspace.schemas
        return copy.deepcopy(schemas)

    def get_schema(self, schemaspace_name_or_id: str, schema_name: str) -> dict:
        """Returns the specified schema for the specified schemaspace."""
        self._validate_schemaspace(schemaspace_name_or_id)

        schemaspace = self.schemaspaces.get(schemaspace_name_or_id.lower())
        schemas = schemaspace.schemas
        if schema_name not in schemas.keys():
            raise SchemaNotFoundError(schemaspace_name_or_id, schema_name)
        schema_json = schemas.get(schema_name)
        return copy.deepcopy(schema_json)

    def get_schemaspace(self, schemaspace_name_or_id: str) -> 'Schemaspace':
        """Returns the Schemaspace instance associated with the given name or id."""
        self._validate_schemaspace(schemaspace_name_or_id)
        return copy.deepcopy(self.schemaspaces.get(schemaspace_name_or_id.lower()))

    def clear_all(self) -> None:
        """Primarily used for testing, this method reloads schemas from initial values. """
        self.log.debug("SchemaManager: Reloading all schemas for all schemaspaces.")
        self._load_schemaspace_schemas()

    def _validate_schemaspace(self, schemaspace_name_or_id: str) -> None:
        """Ensures the schemaspace is valid and raises ValueError if it is not."""
        if schemaspace_name_or_id.lower() not in self.schemaspaces:
            raise ValueError(f"The schemaspace name or id '{schemaspace_name_or_id}' is not "
                             f"in the list of valid schemaspaces: '{self.get_schemaspace_names()}'!")

    def _load_schemaspace_schemas(self):
        """Gets Schemaspaces and SchemasProviders via entrypoints and validates/loads their schemas."""
        self.schemaspaces: Dict[str, Schemaspace] = {}
        self.schemaspace_id_to_name: Dict[str, str] = {}
        self._load_schemaspaces()
        self._load_schemas_providers()
        # Issue a warning for any "empty" schemaspaces...
        empty_schemaspaces = []
        for schemaspace_name in self.schemaspace_id_to_name.values():
            if len(self.schemaspaces[schemaspace_name].schemas) == 0:
                empty_schemaspaces.append(self.schemaspaces[schemaspace_name].name)  # Preserve case
        if len(empty_schemaspaces) > 0:
            self.log.warning(f"The following schemaspaces have no schemas: {empty_schemaspaces}")

    def _load_schemaspaces(self):
        """Loads the Schemaspace instances from entrypoint group 'metadata.schemaspaces'."""
        for schemaspace in SchemaManager._get_schemaspaces():
            # Record the Schemaspace instance and create the name-to-id map
            try:
                # If we're not testing, skip our test schemaspace
                if not self.metadata_testing_enabled and schemaspace.name == METADATA_TEST_SCHEMASPACE:
                    continue
                # instantiate an actual instance of the Schemaspace
                self.log.debug(f"Loading schemaspace '{schemaspace.name}'...")
                schemaspace_instance = schemaspace.load()(parent=self.parent)  # Load an instance
                if not isinstance(schemaspace_instance, Schemaspace):
                    raise ValueError(f"Schemaspace instance '{schemaspace.name}' is not an "
                                     f"instance of '{Schemaspace.__name__}'!")
                # validate the name
                # To prevent a name-to-id lookup, just store the same instance in two locations
                self.schemaspaces[schemaspace_instance.id.lower()] = schemaspace_instance
                self.schemaspaces[schemaspace_instance.name.lower()] = schemaspace_instance
                # We'll keep a map of id-to-name, but this will be primarily used to
                # return the set of schemaspace names (via values()) and lookup a name
                # from its id.
                self.schemaspace_id_to_name[schemaspace_instance.id.lower()] = schemaspace_instance.name.lower()
            except Exception as err:
                # log and ignore initialization errors
                self.log.error(f"Error loading schemaspace '{schemaspace.name}' - {err}")

    def _load_schemas_providers(self):
        """Loads the SchemasProviders instances from entrypoint group 'metadata.schemas'."""
        for schemas_provider_ep in SchemaManager._get_schemas_providers():
            try:
                # If we're not testing, skip our test schemas
                if not self.metadata_testing_enabled and schemas_provider_ep.name == METADATA_TEST_SCHEMASPACE:
                    continue
                # instantiate an actual instance of the processor
                self.log.debug(f"Loading SchemasProvider '{schemas_provider_ep.name}'...")
                schemas_provider = schemas_provider_ep.load()()  # Load an instance
                if not isinstance(schemas_provider, SchemasProvider):
                    raise ValueError(f"SchemasProvider instance '{schemas_provider_ep.name}' is not an "
                                     f"instance of '{SchemasProvider.__name__}'!")
                schemas = schemas_provider.get_schemas()
                for schema in schemas:
                    try:
                        schemaspace_id = schema.get("schemaspace_id")
                        schemaspace_name = schema.get("schemaspace")
                        schema_name = schema.get("name")
                        # Ensure that both schemaspace id and name are registered and both point to same instance
                        if schemaspace_id.lower() not in self.schemaspaces:
                            raise ValueError(f"Schema '{schema_name}' references a schemaspace "
                                             f"'{schemaspace_id}' that is not loaded!")
                        if schemaspace_name.lower() not in self.schemaspaces:
                            raise ValueError(f"Schema '{schema_name}' references a schemaspace "
                                             f"'{schemaspace_name}' that is not loaded!")
                        if self.schemaspaces[schemaspace_id.lower()] != self.schemaspaces[schemaspace_name.lower()]:
                            raise ValueError(f"Schema '{schema_name}' references a schemaspace name "
                                             f"'{schemaspace_name}' and a schemaspace id '{schemaspace_id}' "
                                             f"that are associated with different Schemaspace instances!")

                        self._validate_schema(schemaspace_name, schema_name, schema)
                        # Only add the schema once since schemaspace_name is pointing to the same Schemaspace instance.
                        self.schemaspaces[schemaspace_id.lower()].add_schema(schema)

                    except Exception as schema_err:
                        self.log.error(f"Error loading schema '{schema.get('name', '??')}' for SchemasProvider "
                                       f"'{schemas_provider_ep.name}' - {schema_err}")
            except Exception as provider_err:
                # log and ignore initialization errors
                self.log.error(f"Error loading schemas for SchemasProvider "
                               f"'{schemas_provider_ep.name}' - {provider_err}")

    def _validate_schema(self, schemaspace_name: str, schema_name: str, schema: dict):
        """Validates the given schema against the meta-schema."""
        try:
            self.log.debug(f"Validating schema '{schema_name}' of schemaspace {schemaspace_name}...")
            validate(instance=schema, schema=self._meta_schema, format_checker=draft7_format_checker)
        except ValidationError as ve:
            # Because validation errors are so verbose, only provide the first line.
            first_line = str(ve).partition('\n')[0]
            msg = f"Validation failed for schema '{schema_name}' of " \
                  f"schemaspace '{schemaspace_name}' with error: {first_line}."
            self.log.error(msg)
            raise ValidationError(msg) from ve

    @staticmethod
    def _get_schemaspaces():
        """Wrapper around entrypoints.get_group_all() - primarily to facilitate testing."""
        return get_group_all('metadata.schemaspaces')

    @staticmethod
    def _get_schemas_providers():
        """Wrapper around entrypoints.get_group_all() - primarily to facilitate testing."""
        return get_group_all('metadata.schemas_providers')


class Schemaspace(LoggingConfigurable):
    _id: str
    _name: str
    _display_name: str
    _description: str
    _schemas: Dict[str, Dict]  # use a dict to prevent duplicate entries

    def __init__(self,
                 schemaspace_id: str,
                 name: str,
                 display_name: Optional[str] = None,
                 description: Optional[str] = "",
                 **kwargs):
        super().__init__(**kwargs)

        self._schemas = {}

        # Validate properties
        if not schemaspace_id:
            raise ValueError("Property 'id' requires a value!")

        if not Schemaspace._validate_id(schemaspace_id):
            raise ValueError(f"The value of property 'id' ({schemaspace_id}) does not conform to a UUID!")

        if not name:
            raise ValueError("Property 'name' requires a value!")

        if not Schemaspace._validate_name(name):
            raise ValueError(f"The 'name' property ({name}) must be alphanumeric with dash or underscore only!")

        self._id = schemaspace_id
        self._name = name
        self._display_name = display_name or name
        self._description = description

    @property
    def id(self) -> str:
        """The id (uuid) of the schemaspace"""
        return self._id

    @property
    def name(self) -> str:
        """The name of the schemaspace"""
        return self._name

    @property
    def display_name(self) -> str:
        """The display_name of the schemaspace"""
        return self._display_name

    @property
    def description(self) -> str:
        """The description of the schemaspace"""
        return self._description

    @property
    def schemas(self) -> Dict[str, Dict]:
        """Returns the schemas currently associated with this schemaspace"""
        return self._schemas

    def add_schema(self, schema: Dict) -> None:
        """Associates the given schema to this schemaspace"""
        assert isinstance(schema, dict), "Parameter 'schema' is not a dictionary!"
        self._schemas[schema.get('name')] = schema

    @staticmethod
    def _validate_id(id) -> bool:
        """Validate that id is uuidv4 compliant """
        is_valid = False
        uuidv4_regex = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
        if uuidv4_regex.match(id):
            is_valid = True

        return is_valid

    @staticmethod
    def _validate_name(name) -> bool:
        """Validate that the name adheres to the criteria (alphanumeric, dash, underscore only) """
        is_valid = False
        name_regex = re.compile("^[A-Za-z][0-9A-Za-z_-]*[0-9A-Za-z]$", re.I)
        if name_regex.match(name):
            is_valid = True

        return is_valid


class SchemasProvider(ABC):
    """Abstract base class used to obtain schema definitions from registered schema providers."""

    @abstractmethod
    def get_schemas(self) -> List[Dict]:
        """Returns a list of schemas"""
        pass
