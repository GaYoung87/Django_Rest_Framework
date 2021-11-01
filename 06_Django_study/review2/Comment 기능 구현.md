# Comment 기능 구현

- Comment 모델을 만들어야 합니다.
  - content : 문자열
  - created_at : 시간
  - article : 참조키
- Comment 의 Create, Read, Delete 가 가능해야 합니다.
  - Comment 생성/삭제 동작의 경우 모두 POST 요청으로 동작합니다.
  - Comment 읽기(목록)는및 생성/삭제 동작은 Article 의 읽기(상세보기)에 있습니다.
  - Comment 생성 동작은 모두(View, Template 에서) ModelForm 으로 구현해야 합니다.

