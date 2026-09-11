name: Build Android APK

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout do Código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Configurar Java JDK
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Cache do Buildozer
        uses: actions/cache@v4
        with:
          path: .buildozer
          key: ${{ runner.os }}-buildozer-${{ hashFiles('buildozer.spec') }}
          restore-keys: |
            ${{ runner.os }}-buildozer-

      - name: Instalar Dependências do Sistema
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            build-essential \
            git \
            ffmpeg \
            libsdl2-dev \
            libsdl2-image-dev \
            libsdl2-mixer-dev \
            libsdl2-ttf-dev \
            libportmidi-dev \
            libswscale-dev \
            libavformat-dev \
            libavcodec-dev \
            zlib1g-dev \
            unzip \
            zip \
            autoconf \
            libtool \
            pkg-config \
            libssl-dev

      - name: Instalar Buildozer e Cython
        run: |
          python -m pip install --upgrade pip
          pip install "cython<3.0.0" buildozer

      - name: Compilar APK
        run: |
          buildozer -v android debug

      - name: Salvar APK como Artefato
        uses: actions/upload-artifact@v4
        with:
          name: app-release
          path: bin/*.apk