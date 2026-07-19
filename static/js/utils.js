/* =============================================
   ZY-HR 通用工具函数
   ============================================= */

/** 日期格式化 */
function formatDate(dateStr, fmt = 'YYYY-MM-DD') {
  if (!dateStr) return '-';
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return dateStr;

  const map = {
    'YYYY': d.getFullYear(),
    'MM': String(d.getMonth() + 1).padStart(2, '0'),
    'DD': String(d.getDate()).padStart(2, '0'),
    'HH': String(d.getHours()).padStart(2, '0'),
    'mm': String(d.getMinutes()).padStart(2, '0'),
    'SS': String(d.getSeconds()).padStart(2, '0'),
  };
  let result = fmt;
  for (const [key, val] of Object.entries(map)) {
    result = result.replace(key, val);
  }
  return result;
}

/** 显示加载中状态 */
function showLoading(el) {
  if (typeof el === 'string') el = document.querySelector(el);
  if (!el) return;
  el.innerHTML = '<div class="loading-spinner" style="margin:40px auto"></div>';
}

/** 显示错误状态 */
function showError(el, message = '加载失败') {
  if (typeof el === 'string') el = document.querySelector(el);
  if (!el) return;
  el.innerHTML = `<div class="empty-state"><p>${message}</p></div>`;
}

/** 防抖 */
function debounce(fn, delay = 300) {
  let timer = null;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

/** 剪裁文本 */
function truncate(text, maxLen = 30) {
  if (!text || text.length <= maxLen) return text || '';
  return text.slice(0, maxLen) + '...';
}

/** 深拷贝 */
function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

/** 获取 URL 查询参数 */
function getQueryParam(name) {
  const params = new URLSearchParams(window.location.search);
  return params.get(name);
}
