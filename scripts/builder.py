#!/usr/bin/env python3
"""
The Architect - PDD 2.0 Builder Script

This script reads specifications from the build manifest and prepares
AI prompts for generating code. It gathers context from global specs,
feature specs, and existing target files.

Usage:
    python scripts/builder.py [feature_name]

If no feature name is provided, lists all available features.
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional


class Builder:
    """The Architect - builds code from specifications"""

    def __init__(self, manifest_path: str = "build_manifest.yaml"):
        self.manifest_path = Path(manifest_path)
        self.project_root = self.manifest_path.parent
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> Dict:
        """Load and parse the build manifest"""
        if not self.manifest_path.exists():
            raise FileNotFoundError(
                f"Build manifest not found: {self.manifest_path}\n"
                "Please create build_manifest.yaml in the project root."
            )

        with open(self.manifest_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _read_file(self, file_path: str) -> Optional[str]:
        """Read a file and return its contents, or None if not found"""
        full_path = self.project_root / file_path
        if not full_path.exists():
            return None

        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def _read_files(self, file_list: List[str]) -> Dict[str, Optional[str]]:
        """Read multiple files and return a dictionary of filename to content"""
        result = {}
        for file_path in file_list:
            result[file_path] = self._read_file(file_path)
        return result

    def list_features(self) -> None:
        """List all available features in the manifest"""
        features = self.manifest.get("features", {})

        if not features:
            print("No features defined in build_manifest.yaml")
            return

        print("Available features:")
        print("=" * 70)

        for feature_name, feature_data in features.items():
            status = feature_data.get("status", "unknown")
            description = feature_data.get("description", "No description")
            print(f"\n{feature_name} [{status}]")
            print(f"  {description}")

            spec_files = feature_data.get("spec_files", [])
            if spec_files:
                print(f"  Specs: {', '.join(spec_files)}")

            target_files = feature_data.get("target_files", [])
            if target_files:
                print(f"  Targets: {', '.join(target_files)}")

        print("\n" + "=" * 70)
        print("\nUsage: python scripts/builder.py <feature_name>")

    def build_prompt(self, feature_name: str) -> str:
        """Build an AI prompt for a specific feature"""
        features = self.manifest.get("features", {})

        if feature_name not in features:
            raise ValueError(
                f"Feature '{feature_name}' not found in manifest.\n"
                f"Available features: {', '.join(features.keys())}"
            )

        feature = features[feature_name]

        # Gather global context
        global_context_files = self.manifest.get("global_context", [])
        global_context = self._read_files(global_context_files)

        # Gather feature specs
        spec_files = feature.get("spec_files", [])
        feature_specs = self._read_files(spec_files)

        # Gather existing target files
        target_files = feature.get("target_files", [])
        target_content = self._read_files(target_files)

        # Build the prompt
        prompt = self._format_prompt(
            feature_name, feature, global_context, feature_specs, target_content
        )

        return prompt

    def _format_prompt(
        self,
        feature_name: str,
        feature: Dict,
        global_context: Dict[str, Optional[str]],
        feature_specs: Dict[str, Optional[str]],
        target_content: Dict[str, Optional[str]],
    ) -> str:
        """Format the AI prompt with all gathered information"""
        prompt_parts = []

        # Header
        prompt_parts.append("=" * 70)
        prompt_parts.append(f"AI PROMPT: Build Feature '{feature_name}'")
        prompt_parts.append("=" * 70)
        prompt_parts.append("")

        # Feature description
        prompt_parts.append("## Feature Description")
        prompt_parts.append(feature.get("description", "No description provided"))
        prompt_parts.append("")

        # Global context
        prompt_parts.append("## Global Context")
        prompt_parts.append("")
        for file_path, content in global_context.items():
            prompt_parts.append(f"### {file_path}")
            if content is None:
                prompt_parts.append(f"[File not found: {file_path}]")
            else:
                prompt_parts.append("```")
                prompt_parts.append(content)
                prompt_parts.append("```")
            prompt_parts.append("")

        # Feature specifications
        if feature_specs:
            prompt_parts.append("## Feature Specifications")
            prompt_parts.append("")
            for file_path, content in feature_specs.items():
                prompt_parts.append(f"### {file_path}")
                if content is None:
                    prompt_parts.append(f"[File not found: {file_path}]")
                    prompt_parts.append(
                        "[Note: You may need to create this specification file first]"
                    )
                else:
                    prompt_parts.append("```")
                    prompt_parts.append(content)
                    prompt_parts.append("```")
                prompt_parts.append("")

        # Current implementation (target files)
        prompt_parts.append("## Current Implementation")
        prompt_parts.append("")
        for file_path, content in target_content.items():
            prompt_parts.append(f"### {file_path}")
            if content is None:
                prompt_parts.append(f"[File does not exist yet: {file_path}]")
                prompt_parts.append("[Note: This file will need to be created]")
            else:
                prompt_parts.append("```python")
                prompt_parts.append(content)
                prompt_parts.append("```")
            prompt_parts.append("")

        # Instructions
        prompt_parts.append("## Instructions")
        prompt_parts.append("")
        prompt_parts.append(
            "Based on the global context, feature specifications, and current "
            "implementation above, please:"
        )
        prompt_parts.append("")
        prompt_parts.append(
            "1. Generate or update the code for the target files listed above"
        )
        prompt_parts.append(
            "2. Ensure the implementation follows all coding standards from the global context"
        )
        prompt_parts.append(
            "3. Maintain consistency with the architectural patterns described"
        )
        prompt_parts.append(
            "4. If a file exists, preserve existing functionality while adding/modifying as needed"
        )
        prompt_parts.append(
            "5. If a file doesn't exist, create it with appropriate structure"
        )
        prompt_parts.append("")

        # Target files list
        prompt_parts.append("## Target Files to Generate/Update")
        prompt_parts.append("")
        for file_path in target_content.keys():
            prompt_parts.append(f"- {file_path}")
        prompt_parts.append("")

        # Footer
        prompt_parts.append("=" * 70)
        prompt_parts.append("END OF PROMPT")
        prompt_parts.append("=" * 70)

        return "\n".join(prompt_parts)

    def run(self, feature_name: Optional[str] = None) -> None:
        """Main entry point for the builder"""
        if feature_name is None:
            self.list_features()
            return

        try:
            prompt = self.build_prompt(feature_name)
            print(prompt)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main function"""
    builder = Builder()

    if len(sys.argv) < 2:
        builder.run()
    else:
        feature_name = sys.argv[1]
        builder.run(feature_name)


if __name__ == "__main__":
    main()
