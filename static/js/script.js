// 全局JavaScript功能
$(document).ready(function() {
    // 初始化移动端优化
    initMobileOptimizations();
    
    // 初始化移动端表单优化
    initMobileFormOptimizations();
    
    // 初始化触摸优化
    initTouchOptimizations();
    
    // 初始化移动端滚动优化
    initMobileScrollOptimizations();
    
    // 初始化工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 初始化弹出框
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // 自动隐藏警告框
    $('.alert').each(function() {
        var alert = $(this);
        if (alert.hasClass('alert-success') || alert.hasClass('alert-info')) {
            setTimeout(function() {
                alert.fadeOut('slow');
            }, 5000);
        }
    });

    // 表单验证增强
    $('form').on('submit', function() {
        var form = $(this);
        var submitBtn = form.find('button[type="submit"]');
        
        if (submitBtn.length) {
            var originalText = submitBtn.html();
            submitBtn.prop('disabled', true);
            submitBtn.html('<i class="fas fa-spinner fa-spin me-2"></i>处理中...');
            
            // 如果表单验证失败，恢复按钮状态
            setTimeout(function() {
                if (!form[0].checkValidity()) {
                    submitBtn.prop('disabled', false);
                    submitBtn.html(originalText);
                }
            }, 100);
        }
    });

    // 文件上传增强
    $('input[type="file"]').on('change', function() {
        var input = $(this);
        var files = input[0].files;
        
        if (files.length > 0) {
            var file = files[0];
            var maxSize = 100 * 1024 * 1024; // 100MB
            
            if (file.size > maxSize) {
                showToast('文件大小不能超过100MB', 'error');
                input.val('');
                return;
            }
            
            // 显示文件信息
            var fileInfo = input.siblings('.file-info');
            if (fileInfo.length === 0) {
                fileInfo = $('<div class="file-info mt-2"></div>');
                input.after(fileInfo);
            }
            
            fileInfo.html(
                '<div class="alert alert-info alert-sm">' +
                '<i class="fas fa-file me-2"></i>' +
                '<strong>' + file.name + '</strong><br>' +
                '<small>大小: ' + formatFileSize(file.size) + '</small>' +
                '</div>'
            );
        }
    });

    // 搜索功能增强
    $('input[data-search-target]').on('keyup', function() {
        var searchTerm = $(this).val().toLowerCase();
        var target = $(this).data('search-target');
        
        $(target + ' tbody tr').each(function() {
            var row = $(this);
            var text = row.text().toLowerCase();
            
            if (text.indexOf(searchTerm) > -1) {
                row.show();
            } else {
                row.hide();
            }
        });
    });

    // 复制到剪贴板功能
    $('.copy-btn').on('click', function() {
        var target = $(this).data('copy-target');
        var text = $(target).val() || $(target).text();
        
        copyToClipboard(text);
        showToast('已复制到剪贴板', 'success');
    });

    // 确认删除功能
    $('.delete-btn').on('click', function(e) {
        e.preventDefault();
        var link = $(this);
        var message = link.data('confirm-message') || '确定要删除吗？';
        
        if (confirm(message)) {
            if (link.is('a')) {
                window.location.href = link.attr('href');
            } else if (link.is('form')) {
                link.submit();
            }
        }
    });

    // 表格排序功能
    $('.sortable-table th[data-sort]').on('click', function() {
        var table = $(this).closest('table');
        var column = $(this).data('sort');
        var order = $(this).hasClass('asc') ? 'desc' : 'asc';
        
        // 移除其他列的排序类
        table.find('th').removeClass('asc desc');
        $(this).addClass(order);
        
        sortTable(table, column, order);
    });

    // 批量选择功能
    $('.select-all').on('change', function() {
        var checked = $(this).prop('checked');
        var target = $(this).data('target');
        
        $(target + ' input[type="checkbox"]').prop('checked', checked);
        updateBatchActions();
    });

    $('input[type="checkbox"][data-batch-item]').on('change', function() {
        updateBatchActions();
    });

    // 自动保存功能
    $('form[data-auto-save]').each(function() {
        var form = $(this);
        var saveInterval = form.data('auto-save') || 30000; // 默认30秒
        
        form.find('input, textarea, select').on('change keyup', function() {
            clearTimeout(form.data('saveTimeout'));
            form.data('saveTimeout', setTimeout(function() {
                autoSaveForm(form);
            }, saveInterval));
        });
    });
});

// 工具函数
function showToast(message, type, duration) {
    type = type || 'info';
    duration = duration || 3000;
    
    var alertClass = 'alert-' + (type === 'error' ? 'danger' : type);
    var icon = getAlertIcon(type);
    
    var toast = $('<div class="alert ' + alertClass + ' alert-dismissible fade show position-fixed" ' +
                  'style="top: 20px; right: 20px; z-index: 1050; min-width: 300px;">' +
                  '<i class="' + icon + ' me-2"></i>' + message +
                  '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
                  '</div>');
    
    $('body').append(toast);
    
    setTimeout(function() {
        toast.fadeOut('slow', function() {
            $(this).remove();
        });
    }, duration);
}

function getAlertIcon(type) {
    var icons = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-circle',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle'
    };
    return icons[type] || icons['info'];
}

function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        // 现代浏览器
        return navigator.clipboard.writeText(text);
    } else {
        // 旧版浏览器
        var textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            textArea.remove();
            return Promise.resolve();
        } catch (err) {
            textArea.remove();
            return Promise.reject(err);
        }
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    
    var k = 1024;
    var sizes = ['B', 'KB', 'MB', 'GB'];
    var i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function sortTable(table, column, order) {
    var tbody = table.find('tbody');
    var rows = tbody.find('tr').toArray();
    
    rows.sort(function(a, b) {
        var aVal = $(a).find('[data-sort-value]').eq(column).data('sort-value') ||
                   $(a).find('td').eq(column).text().trim();
        var bVal = $(b).find('[data-sort-value]').eq(column).data('sort-value') ||
                   $(b).find('td').eq(column).text().trim();
        
        // 尝试转换为数字
        if (!isNaN(aVal) && !isNaN(bVal)) {
            aVal = parseFloat(aVal);
            bVal = parseFloat(bVal);
        }
        
        if (order === 'asc') {
            return aVal > bVal ? 1 : -1;
        } else {
            return aVal < bVal ? 1 : -1;
        }
    });
    
    tbody.empty().append(rows);
}

function updateBatchActions() {
    var selectedCount = $('input[type="checkbox"][data-batch-item]:checked').length;
    var batchActions = $('.batch-actions');
    
    if (selectedCount > 0) {
        batchActions.show();
        batchActions.find('.selected-count').text(selectedCount);
    } else {
        batchActions.hide();
    }
}

function autoSaveForm(form) {
    var formData = form.serialize();
    var saveUrl = form.data('save-url') || form.attr('action');
    
    $.ajax({
        url: saveUrl,
        method: 'POST',
        data: formData + '&auto_save=1',
        success: function(response) {
            showToast('表单已自动保存', 'success', 1000);
        },
        error: function() {
            showToast('自动保存失败', 'error', 2000);
        }
    });
}

// 表单验证增强
function validateForm(form) {
    var isValid = true;
    var firstError = null;
    
    // 清除之前的错误状态
    form.find('.is-invalid').removeClass('is-invalid');
    form.find('.invalid-feedback').remove();
    
    // 验证必填字段
    form.find('[required]').each(function() {
        var field = $(this);
        var value = field.val().trim();
        
        if (!value) {
            markFieldInvalid(field, '此字段为必填项');
            isValid = false;
            if (!firstError) firstError = field;
        }
    });
    
    // 验证邮箱格式
    form.find('input[type="email"]').each(function() {
        var field = $(this);
        var value = field.val().trim();
        
        if (value && !isValidEmail(value)) {
            markFieldInvalid(field, '请输入有效的邮箱地址');
            isValid = false;
            if (!firstError) firstError = field;
        }
    });
    
    // 验证电话格式
    form.find('input[type="tel"]').each(function() {
        var field = $(this);
        var value = field.val().trim();
        
        if (value && !isValidPhone(value)) {
            markFieldInvalid(field, '请输入有效的电话号码');
            isValid = false;
            if (!firstError) firstError = field;
        }
    });
    
    // 验证文件大小
    form.find('input[type="file"]').each(function() {
        var field = $(this);
        var files = this.files;
        
        if (files.length > 0) {
            var maxSize = 100 * 1024 * 1024; // 100MB
            for (var i = 0; i < files.length; i++) {
                if (files[i].size > maxSize) {
                    markFieldInvalid(field, '文件大小不能超过100MB');
                    isValid = false;
                    if (!firstError) firstError = field;
                    break;
                }
            }
        }
    });
    
    // 滚动到第一个错误字段
    if (firstError) {
        firstError[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstError.focus();
    }
    
    return isValid;
}

function markFieldInvalid(field, message) {
    field.addClass('is-invalid');
    var feedback = $('<div class="invalid-feedback">' + message + '</div>');
    field.after(feedback);
}

function isValidEmail(email) {
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function isValidPhone(phone) {
    var regex = /^1[3-9]\d{9}$/;
    return regex.test(phone);
}

// 文件拖拽上传
function initDragDrop() {
    $('.file-upload-area').each(function() {
        var dropZone = $(this);
        var fileInput = dropZone.find('input[type="file"]');
        
        dropZone.on('dragover dragenter', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dropZone.addClass('dragover');
        });
        
        dropZone.on('dragleave dragend', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dropZone.removeClass('dragover');
        });
        
        dropZone.on('drop', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dropZone.removeClass('dragover');
            
            var files = e.originalEvent.dataTransfer.files;
            if (files.length > 0) {
                fileInput[0].files = files;
                fileInput.trigger('change');
            }
        });
    });
}

// 数据导出功能
function exportTableData(tableId, filename) {
    var table = $('#' + tableId);
    var csv = [];
    
    // 获取表头
    var headers = [];
    table.find('thead th').each(function() {
        headers.push('"' + $(this).text().trim() + '"');
    });
    csv.push(headers.join(','));
    
    // 获取数据行
    table.find('tbody tr:visible').each(function() {
        var row = [];
        $(this).find('td').each(function() {
            var text = $(this).text().trim().replace(/"/g, '""');
            row.push('"' + text + '"');
        });
        csv.push(row.join(','));
    });
    
    // 下载文件
    var csvContent = csv.join('\n');
    var blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    var link = document.createElement('a');
    
    if (link.download !== undefined) {
        var url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename || 'export.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// 键盘快捷键
$(document).on('keydown', function(e) {
    // Ctrl+S 保存表单
    if (e.ctrlKey && e.which === 83) {
        e.preventDefault();
        var form = $('form:visible').first();
        if (form.length) {
            form.submit();
        }
    }
    
    // ESC 关闭模态框
    if (e.which === 27) {
        $('.modal.show').modal('hide');
    }
});

// 页面加载完成后初始化
$(window).on('load', function() {
    // 初始化拖拽上传
    initDragDrop();
    
    // 初始化移动端表格
    initMobileTables();
    
    // 添加加载完成的动画效果
    $('body').addClass('loaded');
    
    // 初始化懒加载图片
    if ('IntersectionObserver' in window) {
        var imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(function(img) {
            imageObserver.observe(img);
        });
    }
});

// 移动端优化功能
function initMobileOptimizations() {
    // 检测是否为移动设备
    var isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        // 添加移动端类
        $('body').addClass('mobile-device');
        
        // 优化点击事件（避免300ms延迟）
        document.addEventListener('touchstart', function() {}, true);
        
        // 自动调整视口
        if (window.orientation !== undefined) {
            window.addEventListener('orientationchange', function() {
                setTimeout(function() {
                    window.scrollTo(0, 1);
                    initMobileTables();
                }, 100);
            });
        }
        
        // 优化滚动性能
        var isScrolling = false;
        $(window).on('scroll', function() {
            if (!isScrolling) {
                window.requestAnimationFrame(function() {
                    // 在这里可以添加滚动时的优化逻辑
                    isScrolling = false;
                });
                isScrolling = true;
            }
        });
        
        // 优化表单输入
        $('input, textarea').on('focus', function() {
            setTimeout(function() {
                window.scrollTo(0, 0);
                document.body.scrollTop = 0;
            }, 300);
        });
    }
    
    // 监听窗口大小变化
    $(window).on('resize', debounce(function() {
        var newIsMobile = window.innerWidth <= 768;
        if (newIsMobile !== isMobile) {
            isMobile = newIsMobile;
            initMobileTables();
            
            if (isMobile) {
                $('body').addClass('mobile-device');
            } else {
                $('body').removeClass('mobile-device');
            }
        }
    }, 250));
}

// 初始化移动端表格
function initMobileTables() {
    var isMobile = window.innerWidth <= 768;
    
    $('.table-responsive').each(function() {
        var container = $(this);
        var table = container.find('table');
        
        if (!table.length) return;
        
        if (isMobile) {
            convertTableToCards(container, table);
        } else {
            restoreTableFromCards(container, table);
        }
    });
}

// 将表格转换为卡片式布局
function convertTableToCards(container, table) {
    // 检查是否已经转换
    if (container.hasClass('mobile-table-cards')) return;
    
    var headers = [];
    table.find('thead th').each(function() {
        headers.push($(this).text().trim());
    });
    
    var cardsHtml = '';
    table.find('tbody tr').each(function() {
        var row = $(this);
        var cells = row.find('td');
        
        cardsHtml += '<div class="mobile-card-item">';
        
        // 卡片头部（第一列作为标题）
        if (cells.length > 0) {
            cardsHtml += '<div class="mobile-card-header">' + $(cells[0]).html() + '</div>';
        }
        
        cardsHtml += '<div class="mobile-card-content">';
        
        // 其余列作为内容
        for (var i = 1; i < cells.length; i++) {
            if (headers[i]) {
                cardsHtml += '<div class="mobile-card-row">';
                cardsHtml += '<span class="mobile-card-label">' + headers[i] + '</span>';
                cardsHtml += '<span class="mobile-card-value">' + $(cells[i]).html() + '</span>';
                cardsHtml += '</div>';
            }
        }
        
        cardsHtml += '</div></div>';
    });
    
    // 添加卡片容器
    container.append('<div class="mobile-cards-container">' + cardsHtml + '</div>');
    container.addClass('mobile-table-cards');
}

// 恢复表格布局
function restoreTableFromCards(container, table) {
    if (!container.hasClass('mobile-table-cards')) return;
    
    container.find('.mobile-cards-container').remove();
    container.removeClass('mobile-table-cards');
}

// 防抖动函数
function debounce(func, wait) {
    var timeout;
    return function() {
        var context = this;
        var args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            func.apply(context, args);
        }, wait);
    };
}

// 移动端触摸优化
function initTouchOptimizations() {
    // 为所有按钮添加触摸反馈
    $(document).on('touchstart', '.btn, .card, .nav-link', function() {
        $(this).addClass('touch-active');
    });
    
    $(document).on('touchend touchcancel', '.btn, .card, .nav-link', function() {
        var element = $(this);
        setTimeout(function() {
            element.removeClass('touch-active');
        }, 150);
    });
    
    // 优化下拉菜单的触摸交互
    $('.dropdown-toggle').on('touchstart', function(e) {
        e.preventDefault();
        var dropdown = $(this).closest('.dropdown');
        dropdown.toggleClass('show');
        dropdown.find('.dropdown-menu').toggleClass('show');
    });
    
    // 点击空白区域关闭下拉菜单
    $(document).on('touchstart', function(e) {
        if (!$(e.target).closest('.dropdown').length) {
            $('.dropdown').removeClass('show');
            $('.dropdown-menu').removeClass('show');
        }
    });
}

// 移动端表单优化
function initMobileFormOptimizations() {
    // 优化数字输入键盘
    $('input[type="number"], input[type="tel"]').attr('inputmode', 'numeric');
    $('input[type="email"]').attr('inputmode', 'email');
    $('input[type="url"]').attr('inputmode', 'url');
    
    // 优化文本区域自动高度
    $('textarea').each(function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    }).on('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
    
    // 优化选择框显示
    $('select').on('focus', function() {
        $(this).addClass('select-focused');
    }).on('blur', function() {
        $(this).removeClass('select-focused');
    });
    
    // 添加输入框聚焦效果
    $('input, textarea').on('focus', function() {
        $(this).closest('.mb-3, .mb-4').addClass('field-focused');
    }).on('blur', function() {
        $(this).closest('.mb-3, .mb-4').removeClass('field-focused');
    });
}

// 移动端滚动优化
function initMobileScrollOptimizations() {
    // 平滑滚动到顶部按钮
    var scrollToTopBtn = $('<button class="scroll-to-top-btn" style="display: none;"><i class="fas fa-chevron-up"></i></button>');
    $('body').append(scrollToTopBtn);
    
    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            scrollToTopBtn.fadeIn();
        } else {
            scrollToTopBtn.fadeOut();
        }
    });
    
    scrollToTopBtn.click(function() {
        $('html, body').animate({ scrollTop: 0 }, 300);
    });
    
    // 优化长列表滚动
    $('.table-responsive').on('scroll', function() {
        var scrollLeft = $(this).scrollLeft();
        if (scrollLeft > 0) {
            $(this).addClass('scrolled');
        } else {
            $(this).removeClass('scrolled');
        }
    });
}

// 错误处理
window.addEventListener('error', function(e) {
    console.error('页面错误:', e.error);
    // 可以在这里添加错误报告功能
});

// 网络状态监听
window.addEventListener('online', function() {
    showToast('网络连接已恢复', 'success');
});

window.addEventListener('offline', function() {
    showToast('网络连接已断开', 'warning');
});
