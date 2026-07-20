/**
 * ZY-HR 页面初始化脚本
 * 在任意页面引入即可获得导航+登录态
 * 用法: <script src="/static/js/nav.js"></script>
 * 页面只需在需要导航的位置放 <div id="zy-hr-sidebar"></div>
 */
(function() {
    'use strict';

    const TOKEN_KEY = 'Admin-Token';

    function getToken() {
        return localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem('Admin-Token-Session');
    }

    function checkAuth() {
        const token = getToken();
        if (!token) {
            window.location.href = '/login.html';
            return false;
        }
        return true;
    }

    async function loadMenuTree() {
        try {
            const r = await fetch('/sys/menu/tree', {
                headers: { 'Authorization': 'Bearer ' + getToken() }
            });
            const data = await r.json();
            return data.code === 200 ? data.data : [];
        } catch (e) {
            return [];
        }
    }

    // 菜单路径 → 实际HTML文件映射
    const PAGE_MAP = {
        'rencai': '/人才库/talent_bank.html',
        'talent_bank': '/人才库/talent_bank.html',
        'talent_brand': '/人才库/talent_brand.html',
        'talent-detail': '/人才库/talent-detail.html',
        'talent_analysis_dashboard': '/人才库/talent_analysis_dashboard.html',
        'teacher': '/导师帮带看板/teacher.html',
        'master_class': '/大师工作室/master_class.html',
        'studio-detail': '/大师工作室/studio-detail.html',
        'admin-projects': '/课题项目组/admin-projects.html',
        'project-group': '/课题项目组/project-group.html',
        'group_list': '/课题项目组/group_list.html',
        'employee_profile': '/index.html',
        'student_roster': '/index.html',
        'analysis': '/position_competency_analysis.html',
        'competencyAnalysis': '/position_competency_analysis.html',
        'employee_roster': '/index.html',
        'statistics': '/index.html',
    };

    function resolvePath(menuPath) {
        if (!menuPath || menuPath === '#' || menuPath.startsWith('http')) return menuPath || '#';
        // Check page map first
        const key = menuPath.replace(/^\//, '').split('/')[0];
        if (PAGE_MAP[key]) return PAGE_MAP[key];
        // Default: try direct path
        return menuPath.startsWith('/') ? menuPath : '/' + menuPath;
    }

    let activePath = window.location.pathname;

    function renderSidebar(menus) {
        const sidebar = document.getElementById('zy-hr-sidebar');
        if (!sidebar) return;
        let html = '';
        for (const menu of menus) {
            if (menu.visible === false) continue;
            const hasChildren = menu.children && menu.children.length > 0;
            if (hasChildren) {
                html += `
                    <div class="zy-menu-group">
                        <div class="zy-menu-parent" data-id="${menu.id}">
                            <span class="zy-menu-icon">${menu.icon || '📂'}</span>
                            <span class="zy-menu-label">${menu.label}</span>
                            <span class="zy-menu-arrow">▶</span>
                        </div>
                        <div class="zy-menu-children">
                            ${renderChildren(menu.children)}
                        </div>
                    </div>`;
            } else {
                const href = resolvePath(menu.path);
                html += `<a class="zy-menu-item" href="${href}"><span class="zy-menu-icon">${menu.icon || '📄'}</span><span class="zy-menu-label">${menu.label}</span></a>`;
            }
        }
        sidebar.innerHTML = html;
        // 绑定点击事件：父菜单展开/收起
        document.querySelectorAll('.zy-menu-parent').forEach(el => {
            el.addEventListener('click', function() {
                const children = this.nextElementSibling;
                const arrow = this.querySelector('.zy-menu-arrow');
                if (children) {
                    children.classList.toggle('show');
                    if (arrow) arrow.classList.toggle('open');
                }
            });
        });
    }

    function renderChildren(children) {
        if (!children || children.length === 0) return '';
        return children.map(c =>
            `<a class="zy-menu-child" href="${resolvePath(c.path) || '#'}"><span class="zy-menu-dot"></span><span>${c.label}</span></a>`
        ).join('');
    }

    async function renderUserBar() {
        const bar = document.getElementById('zy-hr-userbar');
        if (!bar) return;
        try {
            const r = await fetch('/sys/user/info', {
                headers: { 'Authorization': 'Bearer ' + getToken() }
            });
            const data = await r.json();
            if (data.code === 200 && data.user) {
                const u = data.user;
                bar.innerHTML = `
                    <div class="zy-user-info">
                        <span class="zy-user-avatar">${(u.nickName || u.userName || '?')[0]}</span>
                        <span class="zy-user-name">${u.nickName || u.userName}</span>
                    </div>
                    <button class="zy-btn-logout" onclick="ZYHR.logout()">退出</button>`;
            }
        } catch (e) {
            bar.innerHTML = '';
        }
    }

    window.ZYHR = {
        logout: function() {
            localStorage.removeItem(TOKEN_KEY);
            sessionStorage.removeItem('Admin-Token-Session');
            window.location.href = '/login.html';
        },
        init: async function() {
            if (!checkAuth()) return;
            const menus = await loadMenuTree();
            renderSidebar(menus);
            renderUserBar();
        }
    };

    document.addEventListener('DOMContentLoaded', function() {
        if (document.getElementById('zy-hr-sidebar')) {
            ZYHR.init();
        }
    });
})();
