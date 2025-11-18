#!/usr/bin/env python3
"""
Generic script to convert C# Resource classes from any Aspire.Hosting.* directory to Python classes.
Generates Python equivalents of the C# classes with proper inheritance and documentation.

Usage:
    python convert_aspire_hosting.py <directory_name> [output_file]
    
Examples:
    python convert_aspire_hosting.py Aspire.Hosting.Redis
    python convert_aspire_hosting.py Aspire.Hosting.PostgreSQL postgres_resources.py
    python convert_aspire_hosting.py Aspire.Hosting.Python python_resources.py
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass


@dataclass
class Parameter:
    name: str
    type_name: str
    description: str


@dataclass
class ExtensionMethod:
    name: str
    target_type: str  # The T constraint type
    summary: str
    parameters: List[Parameter]
    return_type: str
    is_static: bool = True


@dataclass
class ClassInfo:
    name: str
    namespace: str
    summary: str
    remarks: str
    example: str
    parameters: List[Parameter]
    base_class: str
    interfaces: List[str]
    visibility: str
    is_sealed: bool = False
    extension_methods: List[ExtensionMethod] = None


class AspireHostingConverter:
    """Generic converter for Aspire.Hosting.* directories."""
    
    # Common base classes and interfaces in Aspire.Hosting
    BASE_CLASSES = {
        'Resource': 'Resource',
        'ContainerResource': 'ContainerResource', 
        'ExecutableResource': 'ExecutableResource',
        'ParameterResource': 'ParameterResource',
    }
    
    INTERFACES = {
        'IResource': 'IResource',
        'IResourceWithConnectionString': 'IResourceWithConnectionString',
        'IResourceWithServiceDiscovery': 'IResourceWithServiceDiscovery',
        'IResourceWithEnvironment': 'IResourceWithEnvironment',
        'IResourceWithArgs': 'IResourceWithArgs',
        'IResourceWithEndpoints': 'IResourceWithEndpoints', 
        'IResourceWithWaitSupport': 'IResourceWithWaitSupport',
        'IResourceWithProbes': 'IResourceWithProbes',
        'IContainerFilesDestinationResource': 'IContainerFilesDestinationResource',
        'IComputeResource': 'IComputeResource',
        'IResourceWithParent': 'IResourceWithParent',
    }
    
    def __init__(self, source_directory: str):
        self.source_directory = Path(source_directory)
        self.classes = []
        self.extension_methods = {}  # Map resource type -> list of methods
        self.package_name = self.source_directory.name
        
    def clean_documentation(self, text: str) -> str:
        """Clean and format documentation text."""
        if not text:
            return ""
        
        # Remove XML tags and comments
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'///\s*', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Handle common patterns
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&amp;', '&', text)
        
        return text
    
    def extract_xml_content(self, xml_content: str, tag: str) -> str:
        """Extract content from XML documentation tags."""
        pattern = f'<{tag}[^>]*>(.*?)</{tag}>'
        match = re.search(pattern, xml_content, re.DOTALL | re.IGNORECASE)
        if match:
            content = self.clean_documentation(match.group(1))
            return content
        return ""
    
    def extract_parameters_from_xml(self, xml_content: str) -> List[Parameter]:
        """Extract parameter documentation from XML."""
        parameters = []
        param_pattern = r'<param name="([^"]*)"[^>]*>(.*?)</param>'
        matches = re.findall(param_pattern, xml_content, re.DOTALL | re.IGNORECASE)
        
        for name, description in matches:
            clean_desc = self.clean_documentation(description)
            parameters.append(Parameter(name=name, type_name="str", description=clean_desc))
            
        return parameters
    
    def parse_class_declaration(self, content: str) -> Optional[Tuple[str, str, List[str], str, bool]]:
        """Parse class declaration to extract name, base class, interfaces, visibility, and sealed status."""
        # First, find the full class declaration line(s)
        class_pattern = r'(public|internal|private)?\s*(sealed\s+)?class\s+(\w+)(?:\([^)]*\))?\s*(?::\s*([^{;]+?))?(?:\s*[{;])'
        match = re.search(class_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not match:
            return None
        
        visibility = match.group(1) or "public"
        is_sealed = bool(match.group(2))
        class_name = match.group(3)
        inheritance_part = match.group(4)
        
        base_class = ""
        interfaces = []
        
        if inheritance_part:
            # Clean up the inheritance part - remove all constructor calls and generic type parameters
            clean_inheritance = re.sub(r'\([^)]*\)', '', inheritance_part)
            clean_inheritance = re.sub(r'<[^>]*>', '', clean_inheritance)  # Remove generic parameters
            parts = [part.strip() for part in clean_inheritance.split(',')]
            
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                    
                # Check if it's an interface (starts with I and next char is uppercase)
                if part.startswith('I') and len(part) > 1 and part[1].isupper():
                    interfaces.append(part)
                else:
                    # It's a base class
                    base_class = part
                        
        return class_name, base_class, interfaces, visibility, is_sealed
    
    def parse_constructor_parameters(self, content: str, class_name: str) -> List[Parameter]:
        """Extract constructor parameters from class declaration."""
        # Look for primary constructor parameters in class declaration
        pattern = rf'class\s+{re.escape(class_name)}\s*\(([^)]+)\)'
        match = re.search(pattern, content)
        
        parameters = []
        if match:
            param_string = match.group(1)
            # Split by comma but respect parentheses
            param_parts = self._split_parameters(param_string)
            
            for part in param_parts:
                part = part.strip()
                if not part:
                    continue
                    
                # Parse "type name" pattern
                tokens = part.split()
                if len(tokens) >= 2:
                    param_type = tokens[0]
                    param_name = tokens[1]
                    parameters.append(Parameter(
                        name=param_name, 
                        type_name=param_type, 
                        description=f"The {param_name} parameter."
                    ))
        
        return parameters
    
    def parse_extension_method(self, method_content: str) -> Optional[ExtensionMethod]:
        """Parse a single extension method from C# content."""
        # Simple approach: extract method name and constraint type
        method_name_pattern = r'public\s+static\s+.*?\s+(\w+)\s*(?:<\w+>)?\s*\([^)]*this\s+IResourceBuilder<(\w+)>'
        name_match = re.search(method_name_pattern, method_content, re.DOTALL)
        
        if not name_match:
            return None
            
        method_name = name_match.group(1)
        generic_type = name_match.group(2)
        
        # Look for where constraint
        constraint_pattern = r'where\s+\w+\s*:\s*([^{;]+)'
        constraint_match = re.search(constraint_pattern, method_content)
        
        target_type = generic_type
        if constraint_match:
            constraint_type = constraint_match.group(1).strip()
            if constraint_type and constraint_type != 'IResource':
                target_type = constraint_type
        
        # Extract method documentation
        summary = ""
        doc_pattern = r'///\s*<summary>(.*?)</summary>'
        doc_match = re.search(doc_pattern, method_content, re.DOTALL)
        if doc_match:
            summary = self.clean_documentation(doc_match.group(1))
        
        # Extract parameters from documentation
        parameters = []
        param_doc_pattern = r'///\s*<param name="([^"]+)"[^>]*>(.*?)</param>'
        param_matches = re.findall(param_doc_pattern, method_content, re.DOTALL)
        
        for param_name, param_desc in param_matches:
            if param_name != 'builder':  # Skip the builder parameter
                clean_desc = self.clean_documentation(param_desc)
                parameters.append(Parameter(
                    name=param_name,
                    type_name="Any",  # Simplified for complex types
                    description=clean_desc if clean_desc else f"The {param_name} parameter."
                ))
        
        return ExtensionMethod(
            name=method_name,
            target_type=target_type,
            summary=summary,
            parameters=parameters,
            return_type="IResourceBuilder<T>"
        )
    
    def parse_builder_extensions(self, file_path: Path) -> List[ExtensionMethod]:
        """Parse all extension methods from a BuilderExtensions file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        extension_methods = []
        
        # Find all public static methods with more flexible pattern
        # Look for method start and find the complete method body
        method_starts = []
        pattern = r'public\s+static\s+.*?\s+(\w+)\s*(?:<\w+>)?\s*\([^)]*this\s+IResourceBuilder<'
        for match in re.finditer(pattern, content):
            method_starts.append((match.start(), match.group(1)))
            
        print(f"    Found {len(method_starts)} potential extension methods")
        if len(method_starts) > 0:
            print(f"    Method names: {[name for _, name in method_starts[:5]]}")  # Show first 5
        
        for i, (start, method_name) in enumerate(method_starts):
            # Find the end of this method (start of next method or end of class)
            end = method_starts[i + 1][0] if i + 1 < len(method_starts) else len(content)
            
            # Extract method content including documentation
            method_start_extended = start
            # Look backwards for documentation
            lines_before_start = content[:start].split('\n')
            for j in range(len(lines_before_start) - 1, -1, -1):
                line = lines_before_start[j].strip()
                if line.startswith('///') or line == '':
                    # Include this line
                    method_start_extended = content.find('\n'.join(lines_before_start[j:]))
                    break
                elif line.startswith('//') or line.startswith('['):
                    # Skip regular comments and attributes
                    continue
                else:
                    # Found non-documentation content, stop
                    break
            
            method_content = content[method_start_extended:end]
            
            # Find actual method end by looking for closing brace
            brace_count = 0
            method_body_start = method_content.find('{')
            if method_body_start != -1:
                for k, char in enumerate(method_content[method_body_start:]):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            method_content = method_content[:method_body_start + k + 1]
                            break
            
            extension_method = self.parse_extension_method(method_content)
            if extension_method:
                extension_methods.append(extension_method)
            else:
                print(f"    Failed to parse method: {method_name}")
        
        return extension_methods
        """Split parameter string by comma, respecting parentheses."""
        parts = []
        current = ""
        paren_depth = 0
        
        for char in param_string:
            if char == '(' :
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif char == ',' and paren_depth == 0:
                parts.append(current)
                current = ""
                continue
            current += char
            
        if current.strip():
            parts.append(current)
            
        return parts
    
    def parse_csharp_file(self, file_path: Path) -> Optional[ClassInfo]:
        """Parse a single C# file and extract class information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
        
        # Extract namespace
        namespace_match = re.search(r'namespace\s+([\w.]+)', content)
        namespace = namespace_match.group(1) if namespace_match else ""
        
        # Find XML documentation before class declaration
        class_pattern = r'(///.*?)?(?:public|internal|private)?\s*(?:sealed\s+)?class\s+(\w+)'
        class_match = re.search(class_pattern, content, re.DOTALL)
        
        summary = ""
        remarks = ""
        example = ""
        xml_parameters = []
        
        if class_match and class_match.group(1):
            xml_content = class_match.group(1)
            summary = self.extract_xml_content(xml_content, 'summary')
            remarks = self.extract_xml_content(xml_content, 'remarks')
            example = self.extract_xml_content(xml_content, 'example')
            xml_parameters = self.extract_parameters_from_xml(xml_content)
        
        # Parse class declaration
        class_info = self.parse_class_declaration(content)
        if not class_info:
            print(f"Warning: Could not parse class declaration in {file_path}")
            return None
            
        class_name, base_class, interfaces, visibility, is_sealed = class_info
        
        # Get constructor parameters if not found in XML
        parameters = xml_parameters
        if not parameters:
            parameters = self.parse_constructor_parameters(content, class_name)
        
        return ClassInfo(
            name=class_name,
            namespace=namespace,
            summary=summary,
            remarks=remarks,
            example=example,
            parameters=parameters,
            base_class=base_class,
            interfaces=interfaces,
            visibility=visibility,
            is_sealed=is_sealed,
            extension_methods=[]
        )
    
    def convert_type_to_python(self, csharp_type: str) -> str:
        """Convert C# types to Python types."""
        type_mapping = {
            'string': 'str',
            'int': 'int',
            'bool': 'bool',
            'double': 'float',
            'float': 'float',
            'object': 'Any',
            'void': 'None',
        }
        
        # Handle nullable types
        if csharp_type.endswith('?'):
            base_type = csharp_type[:-1]
            mapped_type = type_mapping.get(base_type, base_type)
            return f"Optional[{mapped_type}]"
        
        # Handle generic types
        if '<' in csharp_type and '>' in csharp_type:
            return 'Any'
            
        return type_mapping.get(csharp_type, csharp_type)
    
    def generate_python_class(self, class_info: ClassInfo) -> str:
        """Generate Python class definition from ClassInfo."""
        lines = []
        
        # Class definition with inheritance
        inheritance = []
        if class_info.base_class:
            inheritance.append(class_info.base_class)
        for interface in class_info.interfaces:
            inheritance.append(interface)
            
        if inheritance:
            class_def = f"class {class_info.name}({', '.join(inheritance)}):"
        else:
            class_def = f"class {class_info.name}:"
            
        lines.append(class_def)
        
        # Docstring
        docstring_parts = []
        if class_info.summary:
            docstring_parts.append(class_info.summary)
            
        if class_info.remarks:
            docstring_parts.append(f"\n{class_info.remarks}")
            
        if class_info.parameters:
            docstring_parts.append("\nArgs:")
            for param in class_info.parameters:
                docstring_parts.append(f"    {param.name}: {param.description}")
                
        if class_info.example and class_info.example.strip():
            docstring_parts.append(f"\nExample:\n{class_info.example}")
            
        if docstring_parts:
            docstring_content = ''.join(docstring_parts)
            lines.append('    """')
            for line in docstring_content.split('\n'):
                lines.append(f"    {line}")
            lines.append('    """')
        
        # Constructor
        if class_info.parameters:
            params = ['self']
            for param in class_info.parameters:
                param_type = self.convert_type_to_python(param.type_name)
                params.append(f"{param.name}: {param_type}")
            
            constructor = f"    def __init__({', '.join(params)}):"
            lines.append(constructor)
            
            # Constructor body - assign parameters
            for param in class_info.parameters:
                lines.append(f"        self.{param.name} = {param.name}")
                
            # Call super if there's a base class
            if class_info.base_class and class_info.base_class in self.BASE_CLASSES:
                super_params = self._get_super_parameters(class_info)
                if super_params:
                    lines.append(f"        super().__init__({', '.join(super_params)})")
        else:
            lines.append("    def __init__(self):")
            lines.append("        pass")
        
        # Add extension methods as regular methods
        if class_info.extension_methods:
            lines.append("")
            lines.append("    # Extension methods converted from C# builder extensions")
            
            for method in class_info.extension_methods:
                lines.append("")
                lines.append(self._generate_extension_method(method))
            
        return '\n'.join(lines)
    
    def _get_super_parameters(self, class_info: ClassInfo) -> List[str]:
        """Determine appropriate parameters for super() call."""
        if class_info.base_class == 'ContainerResource':
            # ContainerResource typically takes (name, entrypoint=None)
            return ['name'] if any(p.name == 'name' for p in class_info.parameters) else []
        elif class_info.base_class == 'ExecutableResource':
            # ExecutableResource typically takes (name, command, workingDirectory)
            params = []
            for param_name in ['name', 'command', 'workingDirectory']:
                if any(p.name == param_name for p in class_info.parameters):
                    params.append(param_name)
            return params[:3]  # Limit to first 3 that match
        elif class_info.base_class == 'Resource':
            return ['name'] if any(p.name == 'name' for p in class_info.parameters) else []
        else:
            # For custom base classes, try to match first few parameters
            return [p.name for p in class_info.parameters[:2]]
    
    def _generate_extension_method(self, method: ExtensionMethod) -> str:
        """Generate a Python method from an extension method."""
        method_lines = []
        
        # Method signature
        params = ['self']
        for param in method.parameters:
            param_type = self.convert_type_to_python(param.type_name)
            params.append(f"{param.name}: {param_type}")
        
        # Convert method name to snake_case
        python_method_name = self._camel_to_snake(method.name)
        if python_method_name.startswith('with_'):
            python_method_name = python_method_name[5:]  # Remove 'with_' prefix
        
        method_signature = f"    def {python_method_name}({', '.join(params)}) -> '{method.target_type}':"
        method_lines.append(method_signature)
        
        # Method docstring
        if method.summary:
            method_lines.append('        """')
            for line in method.summary.split('\n'):
                method_lines.append(f"        {line}")
            
            if method.parameters:
                method_lines.append('')
                method_lines.append('        Args:')
                for param in method.parameters:
                    method_lines.append(f"            {param.name}: {param.description}")
                    
            method_lines.append('')
            method_lines.append(f"        Returns:")
            method_lines.append(f"            {method.target_type}: This resource instance for method chaining.")
            method_lines.append('        """')
        
        # Method body (placeholder implementation)
        method_lines.append("        # TODO: Implement the actual logic for this extension method")
        for param in method.parameters:
            method_lines.append(f"        # Use parameter: {param.name}")
        method_lines.append("        return self")
        
        return '\n'.join(method_lines)
    
    def _camel_to_snake(self, name: str) -> str:
        """Convert CamelCase to snake_case."""
        # Insert underscore before uppercase letters
        result = re.sub('([A-Z])', r'_\1', name)
        # Remove leading underscore and convert to lowercase
        return result.lstrip('_').lower()
    
    def _split_parameters(self, param_string: str) -> List[str]:
        """Split parameter string by comma, respecting parentheses."""
        parts = []
        current = ""
        paren_depth = 0
        
        for char in param_string:
            if char == '(' :
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif char == ',' and paren_depth == 0:
                parts.append(current)
                current = ""
                continue
            current += char
            
        if current.strip():
            parts.append(current)
            
        return parts
    
    def scan_directory(self) -> List[ClassInfo]:
        """Scan the source directory for C# class files and BuilderExtensions."""
        if not self.source_directory.exists():
            raise FileNotFoundError(f"Source directory not found: {self.source_directory}")
        
        class_files = []
        extension_files = []
        
        # Look for all .cs files
        for cs_file in self.source_directory.glob("*.cs"):
            if cs_file.name.endswith('BuilderExtensions.cs'):
                extension_files.append(cs_file)
            else:
                class_files.append(cs_file)
        
        # Process regular class files
        for file_path in class_files:
            # Skip API files and some common non-resource files
            if file_path.name.startswith('api') or file_path.parent.name == 'api':
                continue
            if file_path.name.endswith('Extensions.cs'):
                continue
            if 'Annotation' in file_path.name:
                continue
            if file_path.name.endswith('ImageTags.cs'):
                continue
            if file_path.name.endswith('Manager.cs'):
                continue
            if file_path.name.endswith('Detector.cs'):
                continue
            if file_path.name.endswith('Configuration.cs'):
                continue
                
            # Only process if file contains "class" keyword
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'class ' not in content:
                        continue
                    # Skip enum files
                    if re.search(r'\benum\s+\w+', content):
                        continue
            except:
                continue
                
            print(f"Processing: {file_path}")
            class_info = self.parse_csharp_file(file_path)
            if class_info:
                self.classes.append(class_info)
            else:
                print(f"Warning: Could not parse {file_path}")
        
        # Process BuilderExtensions files
        for file_path in extension_files:
            print(f"Processing extension methods: {file_path}")
            extension_methods = self.parse_builder_extensions(file_path)
            
            # Group extension methods by target type
            for method in extension_methods:
                if method.target_type not in self.extension_methods:
                    self.extension_methods[method.target_type] = []
                self.extension_methods[method.target_type].append(method)
                print(f"  Found extension method: {method.name} for {method.target_type}")
        
        # Add extension methods to corresponding classes
        for class_info in self.classes:
            if class_info.name in self.extension_methods:
                class_info.extension_methods = self.extension_methods[class_info.name]
                print(f"  Added {len(class_info.extension_methods)} extension methods to {class_info.name}")
                
        return self.classes
    
    def generate_base_classes(self) -> str:
        """Generate base class and interface definitions."""
        return '''# Base classes and interfaces (simplified representations)

class Resource:
    """Base class for all resources."""
    def __init__(self, name: str):
        self.name = name


class ContainerResource(Resource):
    """Base class for container resources."""
    def __init__(self, name: str, entrypoint: Optional[str] = None):
        super().__init__(name)
        self.entrypoint = entrypoint


class ExecutableResource(Resource):
    """Base class for executable resources."""
    def __init__(self, name: str, command: str, working_directory: str = "."):
        super().__init__(name)
        self.command = command
        self.working_directory = working_directory


class ParameterResource(Resource):
    """Represents a parameter resource."""
    def __init__(self, name: str, value: Any = None):
        super().__init__(name)
        self.value = value


# Interfaces (marker classes in Python)

class IResource:
    """Base interface for all resources."""
    pass


class IResourceWithConnectionString(IResource):
    """Interface for resources that provide connection strings."""
    pass


class IResourceWithServiceDiscovery(IResource):
    """Interface for resources that support service discovery."""
    pass


class IResourceWithEnvironment(IResource):
    """Interface for resources that have environment variables.""" 
    pass


class IResourceWithArgs(IResource):
    """Interface for resources that have command line arguments."""
    pass


class IResourceWithEndpoints(IResource):
    """Interface for resources that expose endpoints."""
    pass


class IResourceWithWaitSupport(IResource):
    """Interface for resources that support waiting for readiness."""
    pass


class IResourceWithProbes(IResource):
    """Interface for resources that support health probes."""
    pass


class IContainerFilesDestinationResource(IResource):
    """Interface for resources that can receive container files."""
    pass


class IComputeResource(IResource):
    """Interface for compute resources."""
    pass


class IResourceWithParent(IResource):
    """Interface for resources that have a parent resource."""
    pass

'''
    
    def generate_python_file(self, output_path: str):
        """Generate the complete Python file."""
        lines = []
        
        # Header
        package_display_name = self.package_name.replace('Aspire.Hosting.', '')
        lines.extend([
            '"""',
            f'{package_display_name} Resource Classes converted from {self.package_name}',
            '',
            f'This file contains Python equivalents of the C# Resource classes',
            f'from the .NET {self.package_name} integration.',
            '',
            'These classes represent resources that can be managed and executed',
            'within a distributed application environment.',
            '"""',
            '',
            'from typing import Any, List, Optional, Union, Dict',
            'from abc import ABC, abstractmethod',
            '',
            ''
        ])
        
        # Base classes
        lines.append(self.generate_base_classes())
        lines.append('')
        lines.append(f'# {package_display_name} Resource Classes')
        lines.append('')
        
        # Generate each class
        for class_info in self.classes:
            lines.append(self.generate_python_class(class_info))
            lines.append('')
            lines.append('')
        
        # Utility functions
        lines.extend([
            f'# Utility functions for working with {package_display_name} resources',
            '',
            'def create_resource_by_name(resource_type: str, name: str, **kwargs) -> Any:',
            '    """',
            f'    Create a {package_display_name} resource by type name.',
            '    ',
            '    Args:',
            '        resource_type: The type name of the resource to create',
            '        name: Name of the resource',
            '        **kwargs: Additional arguments for the resource constructor',
            '        ',
            '    Returns:',
            '        Resource instance',
            '    """',
            '    # Map of resource type names to classes',
            '    resource_types = {',
        ])
        
        for class_info in self.classes:
            lines.append(f'        "{class_info.name}": {class_info.name},')
        
        lines.extend([
            '    }',
            '    ',
            '    if resource_type not in resource_types:',
            f'        raise ValueError(f"Unknown {package_display_name} resource type: {{resource_type}}")',
            '    ',
            '    return resource_types[resource_type](name, **kwargs)',
            '',
            '',
            '# Example usage',
            'if __name__ == "__main__":',
            '    # Example: Create resources',
        ])
        
        # Add examples for first few classes
        for class_info in self.classes[:2]:
            if class_info.parameters:
                param_values = []
                for param in class_info.parameters[:3]:  # Limit to first 3 params
                    if param.type_name == 'string' or param.type_name == 'str':
                        param_values.append(f'"{param.name}_value"')
                    else:
                        param_values.append(f'{param.name}_value')
                
                lines.append(f'    {class_info.name.lower()}_example = {class_info.name}({", ".join(param_values)})')
                lines.append(f'    print(f"Created {class_info.name}: {{{class_info.name.lower()}_example.name}}")')
        
        # Write to file
        output_file = Path(output_path)
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            print(f"Successfully generated: {output_file.absolute()}")
            
            # Validate the generated Python code
            try:
                import ast
                ast.parse('\n'.join(lines))
                print("✓ Generated Python code is syntactically valid")
            except SyntaxError as e:
                print(f"⚠ Syntax error in generated code: {e}")
                
        except Exception as e:
            print(f"Error writing to {output_file}: {e}")


def main():
    """Main function to run the converter."""
    parser = argparse.ArgumentParser(
        description='Convert C# Resource classes from Aspire.Hosting.* directories to Python classes.',
        epilog='''
Examples:
  python convert_aspire_hosting.py Aspire.Hosting.Redis
  python convert_aspire_hosting.py Aspire.Hosting.PostgreSQL postgres_resources.py
  python convert_aspire_hosting.py Aspire.Hosting.Python python_resources.py
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('directory', 
                       help='Name of the Aspire.Hosting directory (e.g., Aspire.Hosting.Redis)')
    parser.add_argument('output', nargs='?',
                       help='Output file name (default: <directory_name>_resources.py)')
    parser.add_argument('--src-root', default='src',
                       help='Root source directory (default: src)')
    
    args = parser.parse_args()
    
    # Determine source directory
    script_dir = Path(__file__).parent
    src_dir = script_dir / args.src_root
    source_dir = src_dir / args.directory
    
    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}")
        print(f"Available Aspire.Hosting directories:")
        if src_dir.exists():
            for d in sorted(src_dir.glob("Aspire.Hosting*")):
                if d.is_dir():
                    print(f"  {d.name}")
        sys.exit(1)
    
    # Determine output file
    if args.output:
        output_path = args.output
    else:
        clean_name = args.directory.replace('Aspire.Hosting.', '').lower()
        output_path = f"{clean_name}_resources.py"
    
    print(f"Converting C# Resource classes from: {source_dir}")
    print(f"Output will be written to: {output_path}")
    
    converter = AspireHostingConverter(str(source_dir))
    classes = converter.scan_directory()
    
    if not classes:
        print("No classes found to convert.")
        sys.exit(1)
    
    print(f"Found {len(classes)} classes:")
    for class_info in classes:
        sealed_marker = " (sealed)" if class_info.is_sealed else ""
        print(f"  - {class_info.name} ({class_info.visibility}){sealed_marker}")
    
    converter.generate_python_file(output_path)
    print("\nConversion completed!")


if __name__ == "__main__":
    main()