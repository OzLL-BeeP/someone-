#!/usr/bin/env python3
# Contoh Plugin untuk SOMEONE AI

name = "example"
description = "Contoh plugin untuk testing"
version = "1.0"

def run(args):
    """Fungsi utama plugin"""
    return f"Plugin example berjalan! Args: {args}"

def help():
    return "Usage: /example <teks>"
