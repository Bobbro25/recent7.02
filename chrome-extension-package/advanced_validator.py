#!/usr/bin/env python3
"""
Advanced Chrome Extension Testing Simulator
With increased budget, we can provide comprehensive extension validation
"""

import json
import os
import re
from pathlib import Path

class ExtensionValidator:
    def __init__(self, extension_path):
        self.extension_path = Path(extension_path)
        self.manifest = None
        self.validation_results = []
        
    def load_manifest(self):
        """Load and validate manifest.json"""
        manifest_path = self.extension_path / "manifest.json"
        if not manifest_path.exists():
            self.validation_results.append("❌ CRITICAL: manifest.json not found")
            return False
            
        try:
            with open(manifest_path, 'r') as f:
                self.manifest = json.load(f)
            self.validation_results.append("✅ Manifest loaded successfully")
            return True
        except json.JSONDecodeError as e:
            self.validation_results.append(f"❌ CRITICAL: Invalid JSON in manifest: {e}")
            return False
    
    def validate_manifest_v3(self):
        """Validate Manifest V3 compliance"""
        if not self.manifest:
            return False
            
        required_fields = ["manifest_version", "name", "version"]
        for field in required_fields:
            if field not in self.manifest:
                self.validation_results.append(f"❌ Missing required field: {field}")
                return False
                
        if self.manifest.get("manifest_version") != 3:
            self.validation_results.append("❌ CRITICAL: Not using Manifest V3")
            return False
            
        self.validation_results.append("✅ Manifest V3 compliance verified")
        return True
    
    def validate_permissions(self):
        """Validate extension permissions"""
        permissions = self.manifest.get("permissions", [])
        host_permissions = self.manifest.get("host_permissions", [])
        
        # Check for required permissions
        required_perms = ["activeTab", "storage"]
        for perm in required_perms:
            if perm not in permissions:
                self.validation_results.append(f"⚠️ Missing recommended permission: {perm}")
        
        # Check for overly broad permissions
        if "<all_urls>" in host_permissions:
            self.validation_results.append("⚠️ Using broad <all_urls> permission - ensure justified")
        
        self.validation_results.append(f"✅ Permissions validated: {len(permissions)} declared")
        return True
    
    def validate_content_scripts(self):
        """Validate content script configuration"""
        content_scripts = self.manifest.get("content_scripts", [])
        
        if not content_scripts:
            self.validation_results.append("⚠️ No content scripts defined")
            return True
            
        for i, script in enumerate(content_scripts):
            if "matches" not in script:
                self.validation_results.append(f"❌ Content script {i}: Missing 'matches' field")
                continue
                
            if "js" not in script and "css" not in script:
                self.validation_results.append(f"❌ Content script {i}: No JS or CSS files specified")
                continue
                
            # Validate files exist
            for js_file in script.get("js", []):
                js_path = self.extension_path / js_file
                if not js_path.exists():
                    self.validation_results.append(f"❌ Missing JS file: {js_file}")
                else:
                    self.validation_results.append(f"✅ Found JS file: {js_file}")
                    
            for css_file in script.get("css", []):
                css_path = self.extension_path / css_file
                if not css_path.exists():
                    self.validation_results.append(f"❌ Missing CSS file: {css_file}")
                else:
                    self.validation_results.append(f"✅ Found CSS file: {css_file}")
        
        self.validation_results.append(f"✅ Content scripts validated: {len(content_scripts)} defined")
        return True
    
    def validate_icons(self):
        """Validate icon files"""
        icons = self.manifest.get("icons", {})
        
        required_sizes = ["16", "48", "128"]
        for size in required_sizes:
            if size not in icons:
                self.validation_results.append(f"⚠️ Missing recommended icon size: {size}x{size}")
                continue
                
            icon_path = self.extension_path / icons[size]
            if not icon_path.exists():
                self.validation_results.append(f"❌ Missing icon file: {icons[size]}")
            else:
                self.validation_results.append(f"✅ Found icon {size}x{size}: {icons[size]}")
        
        return True
    
    def validate_popup(self):
        """Validate popup configuration"""
        action = self.manifest.get("action", {})
        
        if "default_popup" in action:
            popup_path = self.extension_path / action["default_popup"]
            if not popup_path.exists():
                self.validation_results.append(f"❌ Missing popup file: {action['default_popup']}")
            else:
                self.validation_results.append(f"✅ Found popup file: {action['default_popup']}")
                # Check for corresponding JS file
                popup_html = popup_path.read_text()
                if 'popup.js' in popup_html:
                    js_path = self.extension_path / "popup.js"
                    if js_path.exists():
                        self.validation_results.append("✅ Found popup.js")
                    else:
                        self.validation_results.append("❌ Missing popup.js referenced in HTML")
        
        return True
    
    def analyze_content_script_quality(self):
        """Analyze content script code quality"""
        content_js_path = self.extension_path / "content.js"
        
        if not content_js_path.exists():
            self.validation_results.append("⚠️ No content.js found for quality analysis")
            return True
            
        content = content_js_path.read_text()
        
        # Check for best practices
        quality_checks = [
            ("MutationObserver", "✅ Uses MutationObserver for dynamic content"),
            ("chrome.storage", "✅ Uses Chrome storage API"),
            ("addEventListener", "✅ Uses proper event listeners"),
            ("class ", "✅ Uses modern class-based architecture"),
            ("async ", "✅ Uses async/await patterns"),
            ("try {", "✅ Includes error handling"),
        ]
        
        for pattern, message in quality_checks:
            if pattern in content:
                self.validation_results.append(message)
        
        # Check for potential issues
        if "innerHTML" in content:
            self.validation_results.append("⚠️ Using innerHTML - ensure XSS protection")
        
        if "eval(" in content:
            self.validation_results.append("❌ CRITICAL: Uses eval() - security risk")
        
        # Check code size
        lines = len(content.split('\n'))
        self.validation_results.append(f"📊 Content script size: {lines} lines")
        
        return True
    
    def validate_store_readiness(self):
        """Check Chrome Web Store submission readiness"""
        store_checks = []
        
        # Name length check
        name = self.manifest.get("name", "")
        if len(name) > 45:
            store_checks.append("⚠️ Extension name too long for store (45 char limit)")
        else:
            store_checks.append(f"✅ Extension name length OK: {len(name)} chars")
        
        # Description length check
        description = self.manifest.get("description", "")
        if len(description) > 132:
            store_checks.append("⚠️ Description too long for store (132 char limit)")
        elif len(description) < 10:
            store_checks.append("⚠️ Description too short")
        else:
            store_checks.append(f"✅ Description length OK: {len(description)} chars")
        
        # Version format check
        version = self.manifest.get("version", "")
        if re.match(r'^\d+\.\d+(\.\d+)?(\.\d+)?$', version):
            store_checks.append(f"✅ Version format OK: {version}")
        else:
            store_checks.append(f"⚠️ Version format may be invalid: {version}")
        
        self.validation_results.extend(store_checks)
        return True
    
    def run_full_validation(self):
        """Run complete validation suite"""
        print("🔍 Running Advanced Chrome Extension Validation...")
        print("=" * 60)
        
        if not self.load_manifest():
            return False
        
        validation_methods = [
            self.validate_manifest_v3,
            self.validate_permissions,
            self.validate_content_scripts,
            self.validate_icons,
            self.validate_popup,
            self.analyze_content_script_quality,
            self.validate_store_readiness,
        ]
        
        for method in validation_methods:
            method()
        
        # Print results
        for result in self.validation_results:
            print(result)
        
        # Summary
        errors = len([r for r in self.validation_results if "❌" in r])
        warnings = len([r for r in self.validation_results if "⚠️" in r])
        successes = len([r for r in self.validation_results if "✅" in r])
        
        print("\n" + "=" * 60)
        print(f"📊 VALIDATION SUMMARY:")
        print(f"   ✅ Passed: {successes}")
        print(f"   ⚠️ Warnings: {warnings}")
        print(f"   ❌ Errors: {errors}")
        
        if errors == 0:
            print("🎉 EXTENSION READY FOR CHROME WEB STORE SUBMISSION!")
        elif errors <= 2:
            print("🔧 Minor issues found - address before submission")
        else:
            print("🚨 Critical issues found - fix before submission")
        
        return errors == 0

def main():
    """Run validation on the Chrome extension"""
    extension_path = "/app/chrome-extension-package"
    
    validator = ExtensionValidator(extension_path)
    validator.run_full_validation()

if __name__ == "__main__":
    main()