FROM ubuntu:22.04 AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8

RUN apt-get update && apt-get install -y \
    libgtk2.0-0 \
    libsdl1.2debian \
    libxxf86vm1 \
    libsm6 \
    libtiff5 \
    libjpeg8 \
    libexpat1 \
    libcanberra-gtk-module \
    fonts-dejavu-core \
    usbutils \
    && rm -rf /var/lib/apt/lists/*

FROM ubuntu:22.04 AS patch

RUN apt-get update && apt-get install -y --no-install-recommends python2.7 \
    && rm -rf /var/lib/apt/lists/*

COPY app/usb-crash-cart-adapter.deb patch-pil.py /tmp/
RUN dpkg-deb -x /tmp/usb-crash-cart-adapter.deb /rootfs \
    && python2.7 /tmp/patch-pil.py /rootfs/opt/usb-crash-cart-adapter/20240517/guts/library.zip

FROM runtime

COPY --from=patch /rootfs/opt /opt

WORKDIR /root
ENTRYPOINT ["/opt/usb-crash-cart-adapter/20240517/guts/dover"]
