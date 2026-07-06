"""
쇼츠 ① v10 — 대화체 다듬은 버전 + AI 이미지 prompt

이전 문제:
- "1년 vs 1주" → 어색 → 자연스러운 대화로
- 발표체 → 친구한테 얘기하듯 대화체
- LoremFlickr 랜덤 사진 → Pollinations AI 생성 이미지로 정확 매칭
"""

SCENES = [
    # HOOK
    dict(id=1, big1="잠깐,", big2="이거 한번 들어보세요",
         caption="", accent="gold",
         narration="잠깐, 이거 한번 들어보세요.",
         prompt="korean man looking serious into camera, dark cinematic background, soft window light, 9:16 portrait, photorealistic, high quality"),

    dict(id=2, big1="한국 직장인", big2="1년에 책 2권",
         caption="대한민국 평균 독서량",
         accent="muted",
         narration="한국 직장인은 1년에 책 두 권 정도 읽거든요?",
         prompt="korean office worker tired at desk piles of paperwork, late evening warm light, melancholic atmosphere, 9:16 portrait, cinematic photography"),

    dict(id=3, big1="근데 머스크는", big2="일주일에 2권",
         caption="같은 두 권, 다른 시간",
         accent="red",
         narration="근데 일론 머스크는요, 일주일에 두 권을 읽는대요.",
         prompt="successful tech entrepreneur reading thick book in modern minimalist office, dramatic golden hour light through large window, 9:16 portrait, cinematic photography, high quality"),

    dict(id=4, big1="이거", big2="좀 이상하지 않아요?",
         caption="",
         accent="gold",
         narration="이거 좀 이상하지 않아요?",
         prompt="man looking puzzled with hand on chin thinking deeply, soft natural lighting, dark moody background, 9:16 portrait, cinematic, photorealistic"),

    # 전개
    dict(id=5, big1="이게", big2="진짜 신기한 거예요",
         caption="",
         accent="info",
         narration="이게 진짜 신기한 거예요.",
         prompt="aha moment realization face man eyes wide open looking up, soft cinematic light, 9:16 portrait, photorealistic detail"),

    dict(id=6, big1="AI 자동화 잘하는 사람이", big2="오히려 책을 더 읽는다는 거",
         caption="",
         accent="green",
         narration="AI 자동화 잘하는 사람이, 오히려 책을 더 많이 읽는다는 거잖아요.",
         prompt="modern entrepreneur with laptop open beside stack of physical books, ambient warm cafe light, contemplative mood, 9:16 portrait, cinematic photography"),

    dict(id=7, big1="이유는", big2="사실 단순해요",
         caption="",
         accent="gold",
         narration="이유는 사실 단순해요.",
         prompt="single light bulb glowing warmly in dark space, conceptual minimalist, 9:16 portrait, cinematic"),

    dict(id=8, big1="ChatGPT 같은 AI는", big2="",
         caption="인터넷 수억 문서를 다 학습해서",
         accent="info",
         narration="ChatGPT 같은 AI는 결국 인터넷에 있는 수억 개 문서를 다 학습해서,",
         prompt="abstract data network neural connections glowing nodes, blue and purple tones, dark background, futuristic, 9:16 portrait, cinematic"),

    dict(id=9, big1="가장 평범한 답을", big2="골라주는 거예요",
         caption="",
         accent="red",
         narration="가장 평범한 답을 골라주는 거예요.",
         prompt="many identical paper documents stacked on top of each other, monotonous repetition, dim lighting, abstract conceptual, 9:16 portrait, cinematic"),

    dict(id=10, big1="누가 물어봐도", big2="비슷비슷한 답",
         caption="",
         accent="muted",
         narration="누가 물어봐도, 비슷비슷한 답이 나올 수밖에 없어요.",
         prompt="crowd of people all looking same direction, identical silhouettes, dramatic backlight, conceptual photography, 9:16 portrait, cinematic"),

    dict(id=11, big1="거기서", big2="한 발 더 나가려면?",
         caption="",
         accent="white",
         narration="근데 거기서 한 발 더 나가려면 어떻게 해야 될까요?",
         prompt="single person stepping forward out of crowd silhouette, dramatic side light, contemplative, 9:16 portrait, cinematic"),

    dict(id=12, big1="한 사람이", big2="10년 파고든 이야기",
         caption="진짜 깊은 통찰",
         accent="gold",
         narration="한 사람이 5년, 10년 그 주제만 파고든, 진짜 깊은 이야기가 필요하잖아요.",
         prompt="old wise scholar surrounded by tall stacks of leather bound books in warm library, golden hour light, dramatic atmosphere, 9:16 portrait, cinematic photography, high detail"),

    dict(id=13, big1="그게 어디 있냐면", big2="책에 있어요",
         caption="",
         accent="green",
         narration="그게 어디 있냐면, 책에 있어요.",
         prompt="open hardcover book on wooden desk with single beam of sunlight, dust particles in air, warm tones, 9:16 portrait, cinematic photography, photorealistic"),

    # 결론
    dict(id=14, big1="AI를 잘 쓰고 싶을수록", big2="책을 더 읽게 돼요",
         caption="",
         accent="info",
         narration="그래서 결국, AI를 잘 쓰고 싶은 사람일수록 책을 더 읽게 되는 거예요.",
         prompt="modern person reading physical book with laptop on side, warm cafe interior light, peaceful focus, 9:16 portrait, cinematic photography"),

    dict(id=15, big1="AI한테는 답을 받고", big2="책에서는 질문을 얻고",
         caption="",
         accent="gold",
         narration="AI한테는 답을 받고, 책에서는 질문을 얻고.",
         prompt="hand on laptop and hand on book at same desk, harmonious composition, warm soft light, 9:16 portrait, cinematic photography"),

    dict(id=16, big1="둘은 반대가 아니라", big2="짝이거든요",
         caption="이게 핵심 메시지",
         accent="gold",
         narration="둘은 반대가 아니라, 짝이거든요.",
         prompt="two hands holding puzzle pieces fitting together, soft warm lighting, conceptual, 9:16 portrait, cinematic photography"),

    # CTA
    dict(id=17, big1="풀버전은", big2="채널에 있어요",
         caption="",
         accent="green",
         narration="풀버전은 채널에 올려놨어요.",
         prompt="phone screen showing youtube channel thumbnails, soft ambient light, modern desk setup, 9:16 portrait, cinematic photography"),

    dict(id=18, big1="검색", big2="\"AI시대 왜 책을\"",
         caption="구독 부탁드려요",
         accent="gold",
         narration="AI시대 왜 책을, 이렇게 검색해보시면 됩니다.",
         prompt="hand holding smartphone showing search bar interface, modern minimalist, soft daylight, 9:16 portrait, photorealistic"),
]


def total():
    return len(SCENES)


if __name__ == "__main__":
    print(f"v10 scenes: {total()}")
    print(f"chars: {sum(len(s['narration']) for s in SCENES)}")
