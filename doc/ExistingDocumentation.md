<!--
SPDX-FileCopyrightText: 2014 Thomas Kalka <thomas.kalka@co-buero.de>
SPDX-FileCopyrightText: 2014 ganafets82 <raabe.stefan@googlemail.com>
SPDX-FileCopyrightText: 2020 hoijui <hoijui.quaero@gmail.com>

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Existing Agrokruh Documentation

- [Project homepage (Slovak)](http://www.agrokruh.sk/)
- [agrokruh (English, video, 8:34)](http://www.youtube.com/watch?v=mYrJ0BJ4Qak)
- [Prezentácia Agrokruh (Slovak, video, 14:37)](http://www.youtube.com/watch?v=Ea4TtM3D0QA)
- [Prezentácia ekologického poľnohospodárstva systémom Agrokruh
  a rozhovor s Jánom Šlinským (Slovak, video, 14:37)](http://archive.org/details/Agrokruh)
- [Agrokruh pre teba, časť 1 z 2 (Slovak, video, 9:16)](http://www.youtube.com/watch?v=IMbGA-nOW64)
- [Agrokruh pre teba, časť 2 z 2 (Slovak, video, 8:52)](http://www.youtube.com/watch?v=Von3EgRGutw)
- [Kreatívne ráno vol. 35 - záznam (Slovak, video, 1:40:19)](http://www.youtube.com/watch?v=2ePhcM1CQa0)
- [Peter Balašov - AGROKRUH:
  Založenie podniku v systéme ekologického (Slovak, video, 1:03:28)](http://www.youtube.com/watch?v=fURltgKS8UU)
- [Z-Day 2011 Bratislava - Prednáška & diskusia (Agrokruh) (Slovak, video, 1:32:49)](http://www.youtube.com/watch?v=E6cbeiZta9U)
- [Sokratov Inštitút - Workshop s Jánom Šlinským (Slovak, video, 2:31)](http://www.youtube.com/watch?v=2P7MGNLz5xE)
- [Komplet mechanizacia (Slovak, video, 3:23)](http://www.youtube.com/watch?v=nStEuHWJE-o)
- [Trochu inak v SND: Ján Šlinský hosťom Adely Banášovej (Slovak, video, 2:26)](http://www.youtube.com/watch?v=-hvIer39SLo)
- [Ján Šlinský - AgroKruh -
  Cohabitat Gathering 2012, Łódź, Poland (Slovak, video, 26:05)](http://www.youtube.com/watch?v=_KY2XpEN0EA)
- [AgroKruh (Jan Slinky) - (Cohabitat Webinar) (Slovak, video, 1:31:37)](https://www.youtube.com/watch?v=UwjPc3UKb4E)

---

Use `ffprobe -show_frames -pretty <stream>` to identify the key frames.

```shell
ffmpeg \
    -i test.mp4 \
    -acodec copy \
    -map 0 \
    -f segment \
    -vcodec copy \
    -reset_timestamps 1 \
    -map 0 \
    OUTPUT%d.mp4
```
