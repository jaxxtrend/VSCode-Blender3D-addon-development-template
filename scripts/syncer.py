#!/usr/bin/env python3
"""
The Fixer - PDD 2.0 Syncer Script

This script reads code from target files and prepares AI prompts for
updating specifications. It ensures specs stay synchronized with
code changes.

Usage:
    python scripts/syncer.py [feature_name]

If no feature name is provided, lists all available features.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

import yaml


class Syncer:
    """The Fixer - syncs specifications from code changes"""

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
        print("\nUsage: python scripts/syncer.py <feature_name>")

    def sync_prompt(self, feature_name: str) -> str:
        """Build an AI prompt for syncing specs from code"""
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

        # Gather current feature specs
        spec_files = feature.get("spec_files", [])
        current_specs = self._read_files(spec_files)

        # Gather current implementation
        target_files = feature.get("target_files", [])
        current_code = self._read_files(target_files)

        # Build the prompt
        prompt = self._format_prompt(
            feature_name, feature, global_context, current_specs, current_code
        )

        return prompt

    def _format_prompt(
        self,
        feature_name: str,
        feature: Dict,
        global_context: Dict[str, Optional[str]],
        current_specs: Dict[str, Optional[str]],
        current_code: Dict[str, Optional[str]],
    ) -> str:
        """Format the AI prompt for syncing specs"""
        prompt_parts = []

        # Header
        prompt_parts.append("=" * 70)
        prompt_parts.append(f"AI PROMPT: Sync Specifications for '{feature_name}'")
        prompt_parts.append("=" * 70)
        prompt_parts.append("")

        # Feature description
        prompt_parts.append("## Feature Description")
        prompt_parts.append(feature.get("description", "No description provided"))
        prompt_parts.append("")

        # Global context (abbreviated)
        prompt_parts.append("## Global Context Reference")
        prompt_parts.append("")
        prompt_parts.append(
            "The following global context files define coding standards and architecture:"
        )
        for file_path in global_context.keys():
            prompt_parts.append(f"- {file_path}")
        prompt_parts.append("")
        prompt_parts.append(
            "Please ensure updated specifications remain consistent with these guidelines."
        )
        prompt_parts.append("")

        # Current implementation (the source of truth)
        prompt_parts.append("## Current Implementation (Source of Truth)")
        prompt_parts.append("")
        for file_path, content in current_code.items():
            prompt_parts.append(f"### {file_path}")
            if content is None:
                prompt_parts.append(f"[File not found: {file_path}]")
                prompt_parts.append(
                    "[Warning: Target file missing - specification may be out of sync]"
                )
            else:
                prompt_parts.append("```python")
                prompt_parts.append(content)
                prompt_parts.append("```")
            prompt_parts.append("")

        # Current specifications
        prompt_parts.append("## Current Specifications (To Be Updated)")
        prompt_parts.append("")
        if not current_specs:
            prompt_parts.append("[No specification files defined for this feature]")
            prompt_parts.append(
                "[Note: You may need to create specification files and add them to build_manifest.yaml]"
            )
            prompt_parts.append("")
        else:
            for file_path, content in current_specs.items():
                prompt_parts.append(f"### {file_path}")
                if content is None:
                    prompt_parts.append(f"[File does not exist: {file_path}]")
                    prompt_parts.append(
                        "[Note: This specification file needs to be created]"
                    )
                else:
                    prompt_parts.append("```")
                    prompt_parts.append(content)
                    prompt_parts.append("```")
                prompt_parts.append("")

        # Instructions
        prompt_parts.append("## Instructions")
        prompt_parts.append("")
        prompt_parts.append(
            "Based on the current implementation (source of truth) and existing "
            "specifications above, please:"
        )
        prompt_parts.append("")
        prompt_parts.append(
            "1. Analyze the current code implementation to understand what it does"
        )
        prompt_parts.append(
            "2. Generate or update specification files to accurately reflect the implementation"
        )
        prompt_parts.append(
            "3. Ensure specifications are clear, accurate, and maintainable"
        )
        prompt_parts.append(
            "4. Document any behavior, edge cases, or design decisions evident in the code"
        )
        prompt_parts.append(
            "5. Keep specifications consistent with global context and architectural guidelines"
        )
        prompt_parts.append(
            "6. If specification files don't exist, create them with appropriate structure"
        )
        prompt_parts.append("")

        # Specification files list
        prompt_parts.append("## Specification Files to Generate/Update")
        prompt_parts.append("")
        if current_specs:
            for file_path in current_specs.keys():
                prompt_parts.append(f"- {file_path}")
        else:
            prompt_parts.append("[No specification files defined - consider creating:")
            prompt_parts.append(f"  - specs/features/{feature_name}.md")
            prompt_parts.append(
                "  Then add this to the feature's spec_files list in build_manifest.yaml]"
            )
        prompt_parts.append("")

        # Additional notes
        if feature.get("notes"):
            prompt_parts.append("## Additional Notes")
            prompt_parts.append("")
            prompt_parts.append(feature["notes"])
            prompt_parts.append("")

        # Footer
        prompt_parts.append("=" * 70)
        prompt_parts.append("END OF PROMPT")
        prompt_parts.append("=" * 70)

        return "\n".join(prompt_parts)

    def run(self, feature_name: Optional[str] = None) -> None:
        """Main entry point for the syncer"""
        if feature_name is None:
            self.list_features()
            return

        try:
            prompt = self.sync_prompt(feature_name)
            print(prompt)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main function"""
    syncer = Syncer()

    if len(sys.argv) < 2:
        syncer.run()
    else:
        feature_name = sys.argv[1]
        syncer.run(feature_name)


if __name__ == "__main__":
    main()
