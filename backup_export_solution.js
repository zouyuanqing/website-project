// 备用导出解决方案 - 如果iframe方式仍有问题可以使用
function backupExportSolution(exportUrl) {
    console.log('🔄 使用备用方案：直接打开新窗口下载');
    
    // 方案1：直接打开新窗口
    const newWindow = window.open(exportUrl, '_blank');
    
    // 检查窗口是否被阻止
    if (!newWindow || newWindow.closed || typeof newWindow.closed == 'undefined') {
        console.warn('⚠️ 弹窗被阻止，尝试直接跳转');
        // 方案2：直接跳转
        window.location.href = exportUrl;
    } else {
        console.log('✅ 新窗口下载已启动');
        // 3秒后关闭新窗口（文件下载通常会很快开始）
        setTimeout(() => {
            if (!newWindow.closed) {
                newWindow.close();
            }
        }, 3000);
    }
}

// 使用方法：在导出函数中替换iframe代码块为：
// backupExportSolution(exportUrl);