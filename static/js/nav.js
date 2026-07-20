/**
 * ZY-HR 导航脚本
 * 登录态检查 + 菜单加载 + 侧边栏导航
 */
(function() {
    'use strict';

    const TOKEN_KEY = 'Admin-Token';
    const API_BASE = window.location.origin;

    // ===================== 工具函数 =====================

    function getToken() {
        return localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem('Admin-Token-Session');
    }

    // ===================== 登录态检查 =====================

    function checkAuth() {
        const token = getToken();
        if (!token) {
            window.location.href = '/login.html';
            return false;
        }
        return true;
    }

    // ===================== 菜单加载 =====================

    async function loadMenuTree() {
        try {
            const r = await fetch(API_BASE + '/sys/menu/tree', {
                headers: { 'Authorization': 'Bearer ' + getToken() }
            });
            const data = await r.json();
            if (data.code === 200) {
                return data.data;
            }
            return [];
        } catch (e) {
            console.error('加载菜单失败:', e);
            return [];
        }
    }

    // ===================== 侧边栏渲染 =====================

    let activePath = window.location.pathname;

    function renderSidebar(menus) {
        const sidebar = document.getElementById('zy-hr-sidebar');
        if (!sidebar) return;

        let html = '';
        for (const menu of menus) {
            if (menu.visible === false) continue;
            const hasChildren = menu.children && menu.children.length > 0;
            const isActive = isMenuActive(menu);

            if (hasChildren) {
                html += `
                    <div class="zy-menu-group">
                        <div class="zy-menu-parent ${isActive ? 'active' : ''}" data-id="${menu.id}">
                            <span class="zy-menu-icon">${menu.icon ? getIconHtml(menu.icon) : '📂'}</span>
                            <span class="zy-menu-label">${menu.label}</span>
                            <span class="zy-menu-arrow ${isActive ? 'open' : ''}">▶</span>
                        </div>
                        <div class="zy-menu-children ${isActive ? 'show' : ''}">
                            ${renderChildren(menu.children)}
                        </div>
                    </div>`;
            } else {
                html += `
                    <a class="zy-menu-item ${isActive ? 'active' : ''}" 
                       href="${menu.path || 'javascript:void(0)'}"
                       data-id="${menu.id}">
                        <span class="zy-menu-icon">${menu.icon ? getIconHtml(menu.icon) : '📄'}</span>
                        <span class="zy-menu-label">${menu.label}</span>
                    </a>`;
            }
        }
        sidebar.innerHTML = html;
        bindMenuEvents();
    }

    function renderChildren(children) {
        if (!children || children.length === 0) return '';
        let html = '';
        for (const child of children) {
            const isActive = isMenuActive(child);
            html += `
                <a class="zy-menu-child ${isActive ? 'active' : ''}" 
                   href="${child.path || 'javascript:void(0)'}"
                   data-id="${child.id}">
                    <span class="zy-menu-dot"></span>
                    <span>${child.label}</span>
                </a>`;
        }
        return html;
    }

    function isMenuActive(menu) {
        if (!menu.path) return false;
        const path = menu.path.startsWith('/') ? menu.path : '/' + menu.path;
        return activePath === path || activePath.startsWith(path + '/');
    }

    function getIconHtml(icon) {
        if (icon === '#' || !icon) return '📄';
        if (icon.startsWith('fa-')) {
            return `<i class="fa ${icon}"></i>`;
        }
        if (icon.startsWith('el-icon-')) {
            return `<i class="${icon}"></i>`;
        }
        return icon;
    }

    function bindMenuEvents() {
        // 父菜单点击展开/收起
        document.querySelectorAll('.zy-menu-parent').forEach(el => {
            el.addEventListener('click', function(e) {
                e.preventDefault();
                const children = this.nextElementSibling;
                const arrow = this.querySelector('.zy-menu-arrow');
                if (children) {
                    children.classList.toggle('show');
                    if (arrow) arrow.classList.toggle('open');
                }
            });
        });
    }

    // ===================== 顶部用户栏 =====================

    async function renderUserBar() {
        const bar = document.getElementById('zy-hr-userbar');
        if (!bar) return;
        try {
            const r = await fetch(API_BASE + '/sys/user/info', {
                headers: { 'Authorization': 'Bearer ' + getToken() }
            });
            const data = await r.json();
            if (data.code === 200 && data.user) {
                const u = data.user;
                bar.innerHTML = `
                    <div class="zy-user-info">
                        <span class="zy-user-avatar">${u.nickName ? u.nickName[0] : '?'}</span>
                        <span class="zy-user-name">${u.nickName || u.userName}</span>
                        <span class="zy-user-dept">${u.deptName || ''}</span>
                    </div>
                    <button class="zy-btn-logout" onclick="ZYHR.logout()">退出</button>
                `;
            }
        } catch (e) {
            bar.innerHTML = `<span style="color:#999;">加载用户信息失败</span>`;
        }
    }

    // ===================== 公开接口 =====================

    window.ZYHR = {
        /** 退出登录 */
        logout: function() {
            localStorage.removeItem('Admin-Token');
            sessionStorage.removeItem('Admin-Token-Session');
            window.location.href = '/login.html';
        },
        /** 初始化导航 */
        init: async function() {
            if (!checkAuth()) return;
            const menus = await loadMenuTree();
            renderSidebar(menus);
            renderUserBar();
        }
    };

    // ===================== 自动初始化 =====================

    document.addEventListener('DOMContentLoaded', function() {
        // 只对需要导航的页面自动初始化
        if (document.getElementById('zy-hr-sidebar')) {
            window.ZYHR.init();
        }
    });

})();
