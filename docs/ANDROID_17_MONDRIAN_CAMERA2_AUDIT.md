# P1 — Camera2 AOSP17 / mondrian preliminary audit

Date: 2026-11-04. Status: **AUDIT ONLY; old PE source not ported, not selected**.

## Source provenance

- Historical PixelExperience-Reborn `packages_apps_Camera2` `seventeen`: `2996abdfce4c5a4f942713f55c55b60d5e58ede9`. Its latest recorded merge is Android 14 `android-14.0.0_r21`, 2024-01-30.
- **Official AOSP17 source of truth**: `https://android.googlesource.com/platform/packages/apps/Camera2/+/refs/tags/android-17.0.0_r1`, tag object `f11b016e1569d39b3b93898a5e1581de2d1007cb`, commit `3adb5275b9791c2128e78969579a69f03fe1ac00`, tree `ef33fbb30b05ddc9189e7ee0fcc40ab89f4efe82`.
- The active PE staged AOSP17 profiles already select `platform/packages/apps/Camera2` in `packages/apps/Camera2`. No old Camera2 source override is enabled.
- Target is AOSP17/API 37 for POCO F5 Pro / Redmi K60 (`mondrian`); standalone source and manifest audits are not a platform build.

## Historical PixelExperience/AOSP changes requiring review

1. The historical Soong `Android.bp` adds `overrides: ["Aperture"]` (commit `10c14c7b645b`, 2022-10-03). The official AOSP17 `Android.bp` does **not** declare this override. **Reject blindly importing**: the optional unported Aperture must not influence system camera packaging.
2. The historical tree contains `Camera2: Do not pass location info for startActivity case` (commit `4ebd97f96391`, 2023-10-27): in `CameraActivity.shouldUseNoOpLocation()`, a capture intent without a calling package uses no-op location rather than granting location. This is a privacy-sensitive behavior and must be rechecked against the actual AOSP17 Java method; do **not** restore an old patch without proving it is missing and testing capture contracts.
3. Old Soong declares `libs: ["org.apache.http.legacy"]`. AOSP17 r1 declares `libs: ["org.apache.http.legacy.stubs.system"]` with `optional_uses_libs: ["org.apache.http.legacy"]`. Preserve official AOSP17 dependency declaration.
4. Official Android17 manifest adds `android:enableOnBackInvokedCallback="false"` to its application; the archived PE manifest lacks it. Preserve official behavior until SDK/back-navigation review.
5. Camera2 uses `sdk_version: "system_current"` and product-specific installation. Android17 source compilation still has to resolve JNI (`libjni_tinyplanet`, `libjni_jpegutil`), camera2 portability, Glide, support libraries and resources from the actual AOSP17 checkout.

## Safeguards and exit criteria

- [x] Compare official AOSP17 commit/tree and historical module/manifest metadata.
- [x] Identify PE camera package override and location-privacy patch provenance.
- [x] Preserve official AOSP17 Camera2 as baseline; staged manifest structure CI rejects a wrong Camera2 source and unintended Aperture selection.
- [x] Maintain source-only static invariants in `tools/verify_a17_camera2_legacy.py`; this is **not** an Android17 compile check.
- [ ] Check whether the old location no-op privacy guard already exists in AOSP17 `CameraActivity.java`, and add a focused regression only if necessary.
- [ ] Complete `m Camera2` and manifest/resource/JNI checks in a full AOSP17 Soong checkout.
- [ ] Verify still/video/secure camera, capture intents, permissions, lens switching, media handling and geotagging on mondrian.
- [ ] Integrate PE changes only by reviewed minimal patch with unit/device evidence; avoid override interactions with Aperture.

**Decision**: keep official AOSP17 Camera2. Historical PE fork is reference material only. No candidate AOSP17 Camera2 fork, no new active manifest profile and no boot/runtime claim arise from this audit.
