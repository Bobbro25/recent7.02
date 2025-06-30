#!/usr/bin/env python3
"""
Chrome Extension Security Analysis Tool
Advanced security validation with increased budget
"""

import re
import os
import json
from pathlib import Path

class SecurityAnalyzer:
    def __init__(self, extension_path):
        self.extension_path = Path(extension_path)
        self.security_issues = []
        self.security_warnings = []
        self.security_passed = []
        
    def analyze_manifest_security(self):
        """Analyze manifest.json for security issues"""
        manifest_path = self.extension_path / "manifest.json"
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        # Check permissions
        permissions = manifest.get("permissions", [])
        host_permissions = manifest.get("host_permissions", [])
        
        # High-risk permissions
        risky_permissions = {
            "tabs": "Can access all browser tabs",
            "history": "Can access browsing history", 
            "bookmarks": "Can access bookmarks",
            "cookies": "Can access cookies",
            "downloads": "Can access downloads",
            "geolocation": "Can access location data"
        }
        
        for perm in permissions:
            if perm in risky_permissions:
                self.security_warnings.append(f"⚠️ High-risk permission: {perm} - {risky_permissions[perm]}")
        
        # Check host permissions
        if "<all_urls>" in host_permissions:
            self.security_warnings.append("⚠️ Extension can access all websites - ensure justified for functionality")
        
        # Check content security policy
        if "content_security_policy" not in manifest:
            self.security_warnings.append("⚠️ No explicit Content Security Policy defined")
        
        self.security_passed.append("✅ Manifest security analysis completed")
        
    def analyze_content_script_security(self):
        """Analyze content scripts for security vulnerabilities"""
        content_js_path = self.extension_path / "content.js"
        
        if not content_js_path.exists():
            return
        
        content = content_js_path.read_text()
        
        # XSS vulnerabilities
        xss_patterns = [
            (r'innerHTML\s*=', "innerHTML assignment - potential XSS risk"),
            (r'outerHTML\s*=', "outerHTML assignment - potential XSS risk"),
            (r'document\.write\s*\(', "document.write usage - XSS risk"),
            (r'eval\s*\(', "eval() usage - code injection risk"),
            (r'Function\s*\(', "Function constructor - code injection risk"),
            (r'setTimeout\s*\(\s*["\']', "setTimeout with string - code injection risk"),
            (r'setInterval\s*\(\s*["\']', "setInterval with string - code injection risk"),
        ]
        
        for pattern, description in xss_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.security_issues.append(f"🚨 SECURITY RISK: {description}")
        
        # Check for DOM sanitization
        if "innerHTML" in content:
            if "textContent" in content or "innerText" in content:
                self.security_passed.append("✅ Uses textContent/innerText for safe DOM updates")
            else:
                self.security_warnings.append("⚠️ Uses innerHTML without apparent sanitization")
        
        # Check for user input handling
        user_input_patterns = [
            r'prompt\s*\(',
            r'confirm\s*\(',
            r'alert\s*\(',
        ]
        
        for pattern in user_input_patterns:
            if re.search(pattern, content):
                self.security_warnings.append("⚠️ Uses user dialogs - consider UX alternatives")
        
        # Check for external requests
        if re.search(r'fetch\s*\(|XMLHttpRequest|ajax', content, re.IGNORECASE):
            self.security_warnings.append("⚠️ Makes external requests - ensure HTTPS and validation")
        
        # Check for local storage usage
        if "localStorage" in content:
            self.security_warnings.append("⚠️ Uses localStorage - consider chrome.storage for extensions")
        
        self.security_passed.append("✅ Content script security analysis completed")
    
    def analyze_popup_security(self):
        """Analyze popup files for security issues"""
        popup_html_path = self.extension_path / "popup.html"
        popup_js_path = self.extension_path / "popup.js"
        
        # Analyze HTML
        if popup_html_path.exists():
            html_content = popup_html_path.read_text()
            
            # Check for inline scripts
            if re.search(r'<script[^>]*>(?!\s*</script>)', html_content, re.IGNORECASE):
                self.security_warnings.append("⚠️ Inline scripts in HTML - use external files")
            
            # Check for external resources
            external_patterns = [
                (r'src\s*=\s*["\']https?://', "External script/resource"),
                (r'href\s*=\s*["\']https?://', "External link/stylesheet"),
            ]
            
            for pattern, description in external_patterns:
                if re.search(pattern, html_content, re.IGNORECASE):
                    self.security_warnings.append(f"⚠️ {description} - ensure trusted sources")
        
        # Analyze popup JS
        if popup_js_path.exists():
            js_content = popup_js_path.read_text()
            
            # Check for chrome API usage
            if "chrome." in js_content:
                if "chrome.tabs" in js_content:
                    self.security_warnings.append("⚠️ Uses chrome.tabs API - ensure minimal permissions")
                if "chrome.storage" in js_content:
                    self.security_passed.append("✅ Uses secure chrome.storage API")
        
        self.security_passed.append("✅ Popup security analysis completed")
    
    def analyze_css_security(self):
        """Analyze CSS files for security issues"""
        css_files = ["content.css", "popup.css"]
        
        for css_file in css_files:
            css_path = self.extension_path / css_file
            if not css_path.exists():
                continue
                
            css_content = css_path.read_text()
            
            # Check for external resources
            if re.search(r'url\s*\(\s*["\']?https?://', css_content, re.IGNORECASE):
                self.security_warnings.append(f"⚠️ {css_file} loads external resources")
            
            # Check for JavaScript in CSS
            if re.search(r'javascript:', css_content, re.IGNORECASE):
                self.security_issues.append(f"🚨 SECURITY RISK: JavaScript URL in {css_file}")
        
        self.security_passed.append("✅ CSS security analysis completed")
    
    def check_privacy_compliance(self):
        """Check for privacy compliance indicators"""
        content_js_path = self.extension_path / "content.js"
        
        if content_js_path.exists():
            content = content_js_path.read_text()
            
            # Check for tracking/analytics
            tracking_patterns = [
                r'google-analytics',
                r'gtag\(',
                r'ga\(',
                r'analytics',
                r'tracking',
                r'telemetry',
            ]
            
            for pattern in tracking_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    self.security_warnings.append(f"⚠️ Possible tracking code detected: {pattern}")
            
            # Check for data collection
            data_patterns = [
                r'navigator\.userAgent',
                r'screen\.',
                r'window\.location',
                r'document\.cookie',
            ]
            
            for pattern in data_patterns:
                if re.search(pattern, content):
                    self.security_warnings.append(f"⚠️ Accesses user data: {pattern}")
        
        self.security_passed.append("✅ Privacy compliance check completed")
    
    def generate_security_report(self):
        """Generate comprehensive security report"""
        print("🔒 CHROME EXTENSION SECURITY ANALYSIS")
        print("=" * 60)
        
        # Run all security checks
        self.analyze_manifest_security()
        self.analyze_content_script_security()
        self.analyze_popup_security()
        self.analyze_css_security()
        self.check_privacy_compliance()
        
        # Print results
        if self.security_issues:
            print("\n🚨 CRITICAL SECURITY ISSUES:")
            for issue in self.security_issues:
                print(f"   {issue}")
        
        if self.security_warnings:
            print("\n⚠️ SECURITY WARNINGS:")
            for warning in self.security_warnings:
                print(f"   {warning}")
        
        if self.security_passed:
            print("\n✅ SECURITY CHECKS PASSED:")
            for passed in self.security_passed:
                print(f"   {passed}")
        
        # Security score
        total_checks = len(self.security_issues) + len(self.security_warnings) + len(self.security_passed)
        security_score = len(self.security_passed) / total_checks * 100 if total_checks > 0 else 0
        
        print("\n" + "=" * 60)
        print(f"🛡️ SECURITY SCORE: {security_score:.1f}%")
        
        if len(self.security_issues) == 0:
            if len(self.security_warnings) <= 3:
                print("✅ SECURITY STATUS: EXCELLENT - Ready for submission")
            else:
                print("⚠️ SECURITY STATUS: GOOD - Address warnings for best practices")
        else:
            print("🚨 SECURITY STATUS: NEEDS ATTENTION - Fix critical issues")
        
        return len(self.security_issues) == 0

def main():
    """Run security analysis"""
    extension_path = "/app/chrome-extension-package"
    
    analyzer = SecurityAnalyzer(extension_path)
    analyzer.generate_security_report()

if __name__ == "__main__":
    main()