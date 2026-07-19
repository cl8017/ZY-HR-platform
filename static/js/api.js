/* =============================================
   ZY-HR 统一 API 请求封装
   ============================================= */

const API_BASE = window.__API_BASE__ || '';

/**
 * 发起 API 请求
 * @param {string} method - HTTP 方法
 * @param {string} path - API 路径
 * @param {object|null} data - 请求体数据
 * @returns {Promise<object>} 响应 JSON
 */
async function apiRequest(method, path, data = null) {
  const url = `${API_BASE}${path}`;
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };

  if (data && method !== 'GET') {
    options.body = JSON.stringify(data);
  }

  // 自动携带登录 Token（若依系统）
  const token = localStorage.getItem('Admin-Token');
  if (token) {
    options.headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const resp = await fetch(url, options);
    if (!resp.ok) {
      throw new Error(`请求失败 (${resp.status})`);
    }
    return resp.json();
  } catch (err) {
    console.error(`[API错误] ${method} ${path}:`, err);
    throw err;
  }
}

/**
 * API 工具对象
 */
const api = {
  get:    (path)           => apiRequest('GET', path),
  post:   (path, data)     => apiRequest('POST', path, data),
  put:    (path, data)     => apiRequest('PUT', path, data),
  delete: (path)           => apiRequest('DELETE', path),
};

/**
 * 获取统一响应中的数据
 * @param {object} resp - API 响应对象
 * @param {*} defaultVal - 默认值
 * @returns {*}
 */
function getData(resp, defaultVal = null) {
  if (resp && resp.code === 200) {
    return resp.data ?? defaultVal;
  }
  console.warn('[API] 非正常响应:', resp);
  return defaultVal;
}
