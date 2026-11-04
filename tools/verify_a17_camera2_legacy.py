#!/usr/bin/env python3
"""Read-only assertions for historical Camera2 source, not an AOSP17 build."""
import re
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
A = "{http://schemas.android.com/apk/res/android}"

def verify(condition, message):
    if not condition:
        raise AssertionError(message)
    print("PASS:", message)

def main():
    bp = (ROOT / "Android.bp").read_text()
    src = (ROOT / "src/com/android/camera/CameraActivity.java").read_text()
    manifest = ET.parse(ROOT / "AndroidManifest.xml").getroot()
    verify(bool(re.search(r'android_app\s*\{\s*name:\s*"Camera2"', bp)),
           "historical Camera2 module exists")
    verify('sdk_version: "system_current"' in bp, "historical system SDK setting")
    verify('overrides: ["Aperture"]' in bp,
           "historical Aperture override identified (MUST NOT PORT BLINDLY)")
    verify('libs: ["org.apache.http.legacy"]' in bp,
           "historical HTTP library dependency identified")
    verify('org.apache.http.legacy.stubs.system' not in bp,
           "current AOSP17 library change remains unported")
    verify("private boolean shouldUseNoOpLocation" in src
           and "if (isCaptureIntent())" in src
           and "callingPackage = mAppContext.getPackageName();" in src,
           "historical capture-intent location privacy guard preserved")
    verify(manifest.get("package") == "com.android.camera2", "Camera2 package name")
    app = manifest.find("application")
    verify(app is not None, "application manifest entry exists")
    verify(app.get(A + "enableOnBackInvokedCallback") is None,
           "historical manifest predates AOSP17 back callback declaration")
    verify(any(x.get(A + "name") == "com.android.camera.SecureCameraActivity"
               and x.get(A + "exported") == "true"
               for x in app.findall("activity")),
           "legacy secure camera activity remains exported")
    for name in ("libjni_tinyplanet", "libjni_jpegutil"):
        verify(f'"{name}"' in bp, "JNI module dependency: " + name)
    print("PASS: source-only legacy assertions; AOSP17 compilation/device testing NOT performed")

if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, ET.ParseError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
