# SV Android App (Native)

이 폴더는 `SV_공략집.html`을 앱 내부 자산으로 포함한 **안드로이드 네이티브 앱(WebView)** 프로젝트입니다.

## 빌드 방법
1. Android Studio에서 `SV_android_app` 폴더를 `Open` 합니다.
2. SDK가 없으면 Android Studio 안내에 따라 설치합니다.
3. `Build > Build Bundle(s) / APK(s) > Build APK(s)` 실행.
4. 생성된 APK를 모바일에 설치합니다.

## 특징
- 인터넷 없이 앱 내부 자산(`app/src/main/assets/SV_files`)으로 실행
- 기존 공략집 UI/데이터 그대로 동작
- 뒤로가기 시 WebView 내 이동, 더 이상 없으면 앱 종료
