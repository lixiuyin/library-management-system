const TokenKey = 'Authorization'

export function getToken() {
  return localStorage.getItem(TokenKey);
}

export function setToken(Authorization) {
  return localStorage.setItem(TokenKey,Authorization);
}

export function removeToken() {
  return localStorage.removeItem(TokenKey);
}
