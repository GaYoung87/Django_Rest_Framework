# Comment와 User간 1 : N 관계 정의

- Comment 모델에 user 필드를 추가하여 1:N 관계를 형성한다.
  - 기존 생성되어있던 comment 가 있을 경우 임의의 사용자 정보로 채운다.
- View 함수에서 comment 생성 시 User 정보를 함께 저장한다.
- Article 상세보기 화면에서 Comment 정보 표현 시 작성자 이름도 함께 보여준다.
- Article 상세보기 화면에서 내가 작성한 Comment 라면 삭제하기 버튼을 보여준다.
- View 함수에서 comment 를 생성한 유저와 요청을 보낸 유저가 같을 경우에만 삭제하기 기능을 수행한다.

