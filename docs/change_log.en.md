# Changelog
v4.10.16
------------------------
Mar 5, 2026

!!! info "New Features 🌱"
    - feat: Added client trusted IP verification capability

!!! summary "Feature Optimization 🚀"
    - perf: Replaced Environment with SandboxedEnvironment to enhance YAML template rendering security

!!! success "Bug Fixes 🐛"
    - fix: Fixed issue where certificate verification was not properly performed for outgoing requests
    - fix: Fixed logical conflict caused by inconsistent field order when exporting resources

v4.10.15
------------------------
January 22, 2026

!!! info "New Features 🌱"
    - feat: Added API Rate Limiting mechanism to enhance interface call stability and security
    - feat: Quick filter capability added to ticket list for improved ticket query and processing efficiency (JumpServer EE)

!!! summary "Feature Optimization 🚀"
    - perf: Upgraded Lion component base image to 1.5.5-trixie
    - perf: Windows asset account password change now supports password verification through pyfreerdp (JumpServer EE)

!!! success "Bug Fixes 🐛"
    - fix: Fixed authentication service not properly validating certificates
    - fix: Fixed issue where corresponding sub-account switching was not created when creating accounts through account templates


v4.10.14
------------------------
December 18, 2025

!!! info "New Features 🌱"
    - feat: JumpServer Client now supports OAuth 2.0 authentication method for improved client login compatibility
    - feat: Virtual applications support VNC protocol connections through local clients (JumpServer EE)

!!! summary "Feature Optimization 🚀"
    - perf: Smart Q&A feature supports custom model configuration to meet different intelligent interaction scenarios
    - perf: Kubernetes platform protocol adds namespace configuration support; users can only access authorized namespaces when connecting for enhanced access control precision

!!! success "Bug Fixes 🐛"
    - fix: Fixed memory leak issue in Razor component (JumpServer EE)
    - fix: Fixed issue where session sharing links could not be copied when connecting through different endpoints


v4.10.13
------------------------
November 20, 2025

!!! info "New Features 🌱"
    - feat: Brand new JumpServer client with smaller size and better user experience (V4)
    - feat: PostgreSQL backend database now supports SSL encrypted connections

!!! summary "Feature Optimization 🚀"
    - perf: All component base images upgraded to Debian 13 (trixie)
    - perf: Supports batch import of weak password lists


v4.10.12
------------------------
October 27, 2025

!!! summary "Feature Optimization 🚀"
    - perf: Optimized password usage mechanism and user permission validation in LDAP service connection testing
    - perf: Optimized user query logic in KoKo session sharing; returns maximum 10 results by default


v4.10.11
------------------------
October 21, 2025

!!! success "Bug Fixes 🐛"
    - fix: Optimized permission verification logic when obtaining SuperConnectionToken


v4.10.10
------------------------
October 16, 2025

!!! info "New Features 🌱"
    - feat: Added data masking feature【Enterprise Edition】Chen and KoKo support all relational databases
    - feat: Magnus only supports MySQL databases

!!! summary "Feature Optimization 🚀"
    - perf: Optimized Razor asset connection stuttering and high memory usage issues (upgraded to FreeRDP3) 【Enterprise Edition】
    - perf: Account push interface adds user group gid parameter

!!! success "Bug Fixes 🐛"
    - fix: Fixed inaccurate display of ACLs rules when selecting all assets in global organizations【Enterprise Edition】


v4.10.9
------------------------
September 24, 2025

!!! summary "Feature Optimization 🚀"
    - perf: Lion file management supports uploading multiple files simultaneously

!!! success "Bug Fixes 🐛"
    - fix: Fixed high memory usage issue in KoKo


v4.10.8
------------------------
September 18, 2025

!!! info "New Features 🌱"
    - feat: Added global resource search feature
    - feat: Supports displaying announcements in popups

!!! summary "Feature Optimization 🚀"
    - perf: Improved cloud sync to avoid releasing assets【Enterprise Edition】
    - perf: Improved RDP true color (24-bit) display

!!! success "Bug Fixes 🐛"
    - fix: Fixed issue where access keys remain valid after user expiration
    - fix: Fixed Chen complex SQL query export failure

v4.10.7
------------------------
September 4, 2025

!!! summary "Feature Optimization 🚀"
    - perf: Encrypted storage of key fields in AccessKey table (migration completed)

!!! success "Bug Fixes 🐛"
    - fix: Fixed user MFA reset failure

v4.10.6
------------------------
August 29, 2025

!!! success "Bug Fixes 🐛"
    - fix: Resolved all components going offline after upgrade
    - fix: Fixed Nec component freezing when using password-only authentication to connect to RealVNC server

v4.10.5
------------------------
August 22, 2025

!!! info "New Features 🌱"
    - feat: Added reporting feature to support visual data analysis and export【Enterprise Edition】
    - feat: Added character search in KoKo to accelerate information finding

!!! summary "Feature Optimization 🚀"
    - perf: User AccessKey stored in encrypted form to improve security
    - perf: Disable Passkey as MFA when SAFE_MODE is enabled for enhanced security

v4.10.4
------------------------
July 16, 2025

!!! summary "Feature Optimization 🚀" 
    - perf: Cloud sync tasks now support switching automatic host information updates【Enterprise Edition】

v4.10.3
------------------------
July 1, 2025

!!! success "Bug Fixes 🐛"
    - fix: Fixed command record count showing 0 after configuring Elasticsearch for command storage
    - fix: Fixed KoKo session showing WebSocket disconnect warning

v4.10.2
------------------------
June 20, 2025

!!! info "New Features 🌱"
    - feat: Support users to set personal language preference
    - feat: Quick commands in Adhoc will hide account name hints when SAFE_MODE=true is enabled

!!! success "Bug Fixes 🐛"
    - fix: Fixed remote application publishing failure
    - fix: Fixed asset type tree nested display anomaly

v4.10.1
------------------------
May 19, 2025

!!! success "Bug Fixes 🐛"
    - fix: Fixed client download failure
    - fix: Fixed watermark enable exception in community edition

v4.10.0
------------------------
May 15, 2025

!!! success "Major Update ⚡️" 

    - feat: Multi-language support: including English, Chinese (Simplified), Chinese (Traditional), Japanese, Portuguese (Brazil), Spanish, Russian, and Korean

!!! info "New Features 🌱"
