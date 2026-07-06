"""
씬별 영문 키워드 매핑 — loremflickr.com에서 매칭 사진을 가져오기 위함.
키워드는 영문이어야 매칭이 잘 됨. 한 씬에 여러 키워드 콤마로 결합.
"""

SCENE_KEYWORDS = {
    # HOOK 0:00–0:42
    1:  "library,books,quiet",
    2:  "smartphone,glow,dark",
    3:  "businessman,thinking,office",
    4:  "open,book,reading",
    # INTRO 0:42–1:10  (메인 메시지)
    5:  "library,golden,light,books",
    6:  "notebook,plan,desk",
    # BODY 1 — AI는 평균 / 책은 깊이
    7:  "library,old,books",
    8:  "data,statistics,abstract",
    9:  "crowd,same,direction",
    10: "old,books,deep,library",
    11: "hidden,door,light",
    12: "reading,book,table",
    13: "starting,line,track",
    14: "library,light,aesthetic",
    15: "transition,road,fork",
    # BODY 2 — 좋은 질문은 사전지식
    16: "question,curiosity,book",
    17: "vocabulary,dictionary,word",
    18: "reading,deep,focus",
    19: "brain,knowledge,book",
    20: "transition,bridge",
    # BODY 3 — 독해력 = 새로운 문해력
    21: "literacy,reading,paper",
    22: "long,document,reading",
    23: "reading,glasses,paper",
    24: "studying,deep,desk",
    # BODY 4 — 트렌드 vs 본질
    25: "old,classic,book",
    26: "ancient,wisdom,statue",
    27: "library,classic,wisdom",
    28: "transition,timeless",
    # BODY 5 — 집중력
    29: "focus,attention,blur",
    30: "concentration,desk,reading",
    31: "calm,morning,book",
    # 실전
    32: "tips,plan,notebook",
    33: "reading,first,book",
    34: "writing,note,book",
    35: "notebook,plan,study",
    # CTA
    36: "library,success,books",
    37: "tools,craft,book",
    38: "reading,coffee,morning",
}
