// quotation_app/static/js/main.js

// 初始化 AOS
AOS.init({
    duration: 800, // 動畫持續時間
    easing: 'ease-in-out', // 動畫效果
    once: true, // 只在第一次滾動時觸發
});

// 返回頂部按鈕功能
const backToTopButton = document.getElementById('backToTop');

// 當用戶滾動超過 300px 時顯示按鈕
window.onscroll = function() {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
};

// 點擊按鈕後平滑滾動回頂部
backToTopButton.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// 閒置自動登出腳本
(function() {
    // 閒置時間設定（例如：20分鐘）
    const idleTime = 20 * 60 * 1000; // 20 分鐘，單位毫秒

    let idleTimer;

    function logout() {
        window.location.href = "/logout/"; // 直接使用 URL，避免在 JS 中使用模板標籤
    }

    function resetIdleTimer() {
        clearTimeout(idleTimer);
        idleTimer = setTimeout(logout, idleTime);
    }

    // 初始化計時器
    resetIdleTimer();

    // 監聽用戶活動
    window.addEventListener('mousemove', resetIdleTimer);
    window.addEventListener('keydown', resetIdleTimer);
    window.addEventListener('click', resetIdleTimer);
    window.addEventListener('scroll', resetIdleTimer);
})();

// 防止使用者通過返回按鈕訪問前一頁
(function() {
    // 推送一個新的歷史狀態，以便捕捉返回按鈕事件
    history.pushState(null, null, location.href);
    window.addEventListener('popstate', function(event) {
        // 當使用者按下返回按鈕時，自動登出
        window.location.href = "/logout/"; // 直接使用 URL
    });
})();
