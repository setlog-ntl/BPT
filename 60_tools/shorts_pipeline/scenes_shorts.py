"""
쇼츠 ① 충격 통계형 — 2분 (120초)

16씬 구조:
  HOOK 0:00-0:05 (3씬, 5s)
  전개 0:05-1:10 (8씬, 65s)
  결론 1:10-1:50 (3씬, 40s)
  CTA  1:50-2:00 (2씬, 10s)
"""

SCENES = [
    # HOOK 0:00-0:05 — 충격 통계
    dict(id=1, part="HOOK", duration=2,
         big1="한국 직장인",
         big2="1년에 2권",
         caption="대한민국 평균 독서량",
         keyword="korean,office,worker,desk,tired",
         narration="한국 직장인은, 1년에 책 두 권을 읽습니다.",
         accent="muted"),
    dict(id=2, part="HOOK", duration=2,
         big1="일론 머스크",
         big2="1주에 2권",
         caption="세계에서 가장 바쁜 사람",
         keyword="elon,musk,silicon,valley,tech",
         narration="그런데 일론 머스크는, 일주일에 두 권이에요.",
         accent="red"),
    dict(id=3, part="HOOK", duration=2,
         big1="1년 vs 1주",
         big2="50배 차이",
         caption="",
         keyword="comparison,scale,big,number",
         narration="1년 vs 1주. 50배 차이.",
         accent="gold"),

    # 전개 0:05-1:10
    dict(id=4, part="BODY", duration=5,
         big1="이상하지 않아요?",
         big2="",
         caption="AI 시대에",
         keyword="thinking,man,question",
         narration="이상하지 않아요? AI 시대에",
         accent="white"),
    dict(id=5, part="BODY", duration=8,
         big1="누구보다 빨리",
         big2="자동화하는 사람이",
         caption="",
         keyword="automation,ai,robot,future",
         narration="누구보다 빨리 자동화하고 있는 사람이,",
         accent="info"),
    dict(id=6, part="BODY", duration=8,
         big1="누구보다 더",
         big2="책을 읽어요",
         caption="",
         keyword="reading,book,man,library",
         narration="누구보다 책을 더 많이 읽고 있다는 거.",
         accent="green"),
    dict(id=7, part="BODY", duration=4,
         big1="이유는 하나",
         big2="",
         caption="",
         keyword="reason,why,one",
         narration="이유는 하나예요.",
         accent="gold"),
    dict(id=8, part="BODY", duration=10,
         big1="AI는",
         big2="평균값만 준다",
         caption="수억 문서의 통계적 평균",
         keyword="data,average,statistics,abstract",
         narration="AI는 평균값만 줍니다. 인터넷 수억 문서를 학습해서 가장 무난한 답을 주는 거죠.",
         accent="red"),
    dict(id=9, part="BODY", duration=4,
         big1="거기서 벗어나려면?",
         big2="",
         caption="",
         keyword="escape,break,out,arrow",
         narration="거기서 벗어나려면?",
         accent="white"),
    dict(id=10, part="BODY", duration=12,
         big1="한 사람이",
         big2="5년·10년 파고든",
         caption="비대칭 정보",
         keyword="deep,research,decade,study",
         narration="한 사람이 5년, 10년 파고든 비대칭 정보가 필요한데,",
         accent="gold"),
    dict(id=11, part="BODY", duration=8,
         big1="그건 책에만",
         big2="있어요",
         caption="",
         keyword="library,old,books,classic",
         narration="그건 책에만 있어요.",
         accent="green"),

    # 결론 1:10-1:50
    dict(id=12, part="CONCLUSION", duration=10,
         big1="AI를 잘 쓰고 싶은",
         big2="사람일수록",
         caption="",
         keyword="successful,man,entrepreneur",
         narration="그러니까 AI를 잘 쓰고 싶은 사람일수록,",
         accent="info"),
    dict(id=13, part="CONCLUSION", duration=8,
         big1="책을 더",
         big2="읽어야 합니다",
         caption="",
         keyword="reading,deep,focus,bookstore",
         narration="책을 더 읽어야 한다는 거예요.",
         accent="gold"),
    dict(id=14, part="CONCLUSION", duration=10,
         big1="AI는 답을 주고",
         big2="책은 질문을 만든다",
         caption="이 한 문장이 핵심",
         keyword="library,wisdom,answer,question",
         narration="AI는 답을 주고, 책은 질문을 만들거든요.",
         accent="gold"),

    # CTA 1:50-2:00
    dict(id=15, part="CTA", duration=5,
         big1="10분 풀버전",
         big2="채널에서",
         caption="",
         keyword="youtube,channel,subscribe",
         narration="10분 풀버전은 채널 영상에서.",
         accent="green"),
    dict(id=16, part="CTA", duration=5,
         big1="검색",
         big2="\"AI시대 왜 책을\"",
         caption="구독·좋아요 부탁드려요",
         keyword="search,bar,find,magnify",
         narration="AI시대 왜 책을, 검색해주세요.",
         accent="gold"),
]


def total_duration():
    return sum(s["duration"] for s in SCENES)


if __name__ == "__main__":
    t = total_duration()
    print(f"Scenes: {len(SCENES)}")
    print(f"Planned total: {t}s = {t//60}:{t%60:02d}")
    chars = sum(len(s["narration"]) for s in SCENES)
    print(f"Narration chars: {chars}")
