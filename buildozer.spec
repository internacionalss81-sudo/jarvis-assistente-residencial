name: Build Android APK

on:
  push:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            python3-pip \
            build-python \
            git \
            zip \
            unzip \
            autoconf \
            libtool \
            pkg-config \
            zlib1g-dev \
            libncurses5-dev \
            libncursesw5-dev \
            libffi-dev \
            libssl-dev

      - name: Install Buildozer and dependencies
        run: |
          pip install --upgrade pip
          pip install buildozer cython

      # Se o buildozer baixar o SDK/NDK, este passo garante que as licenças sejam aceitas
      - name: Accept Android SDK licenses
        run: |
          mkdir -p ~/.buildozer/android/platform/android-sdk
          yes | sdkmanager --licenses || true

      - name: Build with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          command: android debug

      - name: Upload APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: package
          path: bin/*.apk
