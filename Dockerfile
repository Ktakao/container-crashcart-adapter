FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for StarTech Crash Cart Adapter software
RUN apt update && apt install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxss1 \
    libxrandr2 \
    libgtk2.0-0 \
    libsdl1.2debian \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    udev \
    xdg-utils \
    usbutils \
    curl \
    file \
    sudo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Environment setup for XDG
ENV XDG_DATA_DIRS=/usr/share
RUN mkdir -p /usr/share/desktop-directories /usr/share/applications

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]