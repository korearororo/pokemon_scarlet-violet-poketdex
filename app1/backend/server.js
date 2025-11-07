// express 라이브러리를 불러옵니다.
const express = require('express');
const cors = require('cors');

// express 앱을 생성합니다.
const app = express();

// 서버를 실행할 포트 번호를 설정합니다.
// React가 3000번대(Vite는 5173)를 쓰니, 겹치지 않게 4000번으로 설정합니다.
const port = 4000;

// 모든 요청에 대해 CORS를 허용합니다.
app.use(cors());
// JSON 형식의 요청 본문을 파싱할 수 있도록 설정합니다.
app.use(express.json());

// 임시 데이터 (나중에는 데이터베이스와 연동합니다)
let todos = [
  { id: 1, task: 'React 복습하기', done: false },
  { id: 2, task: 'Node.js 서버 만들기', done: true },
  { id: 3, task: '운동가기', done: false },
];

// GET 요청이 '/api/todos' 경로로 들어왔을 때의 처리 규칙
app.get('/api/todos', (req, res) => {
  // res.json()은 우리가 가진 데이터를 JSON 형태로 응답(response)해주는 기능입니다.
  res.json(todos);
});


// 서버가 4000번 포트에서 실행되도록 설정하고, 실행되면 메시지를 출력합니다.
app.listen(port, () => {
  console.log(`🚀 서버가 http://localhost:${port} 에서 실행 중입니다.`);
});

