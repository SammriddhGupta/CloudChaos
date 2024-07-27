import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function RedirectPage() {

  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const searchParams = new URLSearchParams(location.hash.substring(1));
    let code = searchParams.get('access_token');
    console.log(code)
    if (code) {
      console.log('Extracted code:', code);
      localStorage.setItem('auth_token', code);
      let data = parseJwt(code);
      localStorage.setItem('username', data.username);
      console.log(data.username);
    } else {
      console.error('No code parameter found - setting code to 1');
      code = 1;
    }
    navigate('/dashboard'); 
  }, [navigate, location.search, location.hash]); 

  return null;
}

function parseJwt (token) {
  var base64Url = token.split('.')[1];
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
  console.log(JSON.parse(jsonPayload));
  return JSON.parse(jsonPayload);
}

export default RedirectPage;