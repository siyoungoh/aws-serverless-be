# aws-serverless-be
SCC AWS 로 서버리스 백엔드 배포 실습코드

## Quiz 
### Ver.1028
```md
- api 주소
/dev/board

- 기능
글쓰기

- 테이블 스팩
create table bbs
(
	idx int auto_increment,
	title varchar(100) not null,
	content text not null,
  regDate datetime default CURRENT_TIMESTAMP not null
	constraint bbs_pk
		primary key (idx)
);
```
- READ시 Query 사용 : `select title, content, DATE_FORMAT(regDate, '%Y%m%d') as regDate from bbs`

### Ver.1029
```md
- api 주소
/dev/bbs
- 기능
글쓰기
- 테이블 스팩
create table bbs
(
	idx int auto_increment,
	title varchar(100) not null,
	content text not null,
        regDate varchar(8) not null,
	constraint bbs_pk
		primary key (idx)
);
```
- Query 수업자료 그대로 사용
