import * as jose from 'https://cdn.jsdelivr.net/npm/jose@4/dist/browser/index.min.js';

async function fetchPublicKey() {
  const r = await fetch('/public_key');
  if (!r.ok) throw new Error('Não foi possível obter chave pública');
  return await r.text();
}

function showAlert(msg) {
  alert(msg);
}

async function registerUser(e) {
  e.preventDefault();
  const username = document.getElementById('reg-username').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const password = document.getElementById('reg-password').value;

  const r = await fetch('/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, email, password})
  });

  if (r.status === 201) {
    showAlert('Cadastro realizado com sucesso. Faça login.');
    e.target.reset();
    window.location.href = '/static/index.html'; // redireciona para login
  } else {
    const body = await r.json();
    showAlert('Erro no cadastro: ' + (body.detail || body.message || JSON.stringify(body)));
  }
}

async function loginUser(e) {
  e.preventDefault();
  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;

  const r = await fetch('/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  });

  if (r.status !== 200) {
    const body = await r.json().catch(()=>({detail:'Resposta inesperada'}));
    showAlert('Login falhou: ' + (body.detail || JSON.stringify(body)));
    return;
  }

  const body = await r.json();
  const token = body.access_token;

  try {
    const pubPEM = await fetchPublicKey();
    const pubKey = await jose.importSPKI(pubPEM, 'RS256');
    await jose.jwtVerify(token, pubKey);

    document.cookie = `token=${token}; max-age=${body.expires_in}; path=/`;

    window.location.href = '/static/profile.html';
  } catch (err) {
    console.error(err);
    showAlert('Token inválido ou assinado com chave diferente. Voltando à página inicial.');
    window.location.href = '/static/index.html';
  }
}

/* listeners (só adiciona se o form existir na página atual) */
const registerForm = document.getElementById('registerForm');
if (registerForm) {
  registerForm.addEventListener('submit', registerUser);
}

const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', loginUser);
}
