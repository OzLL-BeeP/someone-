#!/usr/bin/env python3
# Sandbox - Check Code Before Execution
# By: K1dz

import re
import ast
import subprocess
import tempfile
import os

class Sandbox:
    @staticmethod
    def check_python(code):
        """Cek keamanan kode Python"""
        warnings = []
        errors = []
        suggestions = []
        
        # Cek syntax
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(f"Syntax error: {e}")
            return {"status": "error", "errors": errors}
        
        # Cek dangerous imports
        dangerous_imports = ["os", "subprocess", "shutil", "sys", "eval", "exec"]
        for imp in dangerous_imports:
            if f"import {imp}" in code or f"from {imp}" in code:
                warnings.append(f"⚠️ Dangerous import detected: {imp}")
                suggestions.append(f"Consider using a safer alternative for {imp}")
        
        # Cek eval/exec
        if "eval(" in code or "exec(" in code:
            errors.append("❌ eval() or exec() detected - potentially dangerous")
            suggestions.append("Use ast.literal_eval() instead")
        
        # Cek file operations
        if "open(" in code:
            warnings.append("⚠️ File operation detected")
            suggestions.append("Ensure file paths are validated")
        
        # Cek infinite loops
        if "while True" in code and "break" not in code:
            warnings.append("⚠️ Potential infinite loop")
            suggestions.append("Add a break condition or timeout")
        
        return {
            "status": "warning" if warnings else "safe",
            "warnings": warnings,
            "errors": errors,
            "suggestions": suggestions
        }
    
    @staticmethod
    def check_bash(code):
        """Cek keamanan kode Bash"""
        warnings = []
        errors = []
        suggestions = []
        
        dangerous_cmds = ["rm -rf", "dd if=", "mkfs", "format", "sudo", "chmod 777"]
        for cmd in dangerous_cmds:
            if cmd in code:
                errors.append(f"❌ Dangerous command detected: {cmd}")
                suggestions.append("This command can cause irreversible damage")
        
        # Cek curl/wget to unknown
        if "curl" in code or "wget" in code:
            warnings.append("⚠️ Download command detected")
            suggestions.append("Verify the source before downloading")
        
        return {
            "status": "error" if errors else "warning" if warnings else "safe",
            "warnings": warnings,
            "errors": errors,
            "suggestions": suggestions
        }
    
    @staticmethod
    def check_code(code, lang="python"):
        """Main sandbox check"""
        if lang == "python":
            return Sandbox.check_python(code)
        elif lang == "bash":
            return Sandbox.check_bash(code)
        else:
            return {"status": "unknown", "warnings": [], "errors": ["Unsupported language"]}
    
    @staticmethod
    def execute_safe(code, lang="python", timeout=10):
        """Execute code in sandbox with timeout"""
        try:
            if lang == "python":
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    tmp_file = f.name
                
                result = subprocess.run(
                    ["python3", tmp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                os.unlink(tmp_file)
                return result.stdout or result.stderr or "✅ Executed successfully (no output)"
            
            elif lang == "bash":
                result = subprocess.run(
                    ["bash", "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                return result.stdout or result.stderr or "✅ Executed successfully (no output)"
            
            else:
                return "❌ Unsupported language"
                
        except subprocess.TimeoutExpired:
            return "❌ Execution timeout"
        except Exception as e:
            return f"❌ Error: {str(e)}"
