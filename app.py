<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VocabGram - 預覽</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; -webkit-tap-highlight-color: transparent; background-color: #fafafa; }
        .ig-gradient { background: radial-gradient(circle at 30% 107%, #fdf497 0%, #fdf497 5%, #fd5949 45%, #d6249f 60%, #285AEB 90%); }
        .active-tab { color: #262626 !important; border-top: 2px solid #262626; margin-top: -2px; }
        .card-inner { transition: transform 0.6s; transform-style: preserve-3d; }
        .flipped { transform: rotateY(180deg); }
        .backface-hidden { backface-visibility: hidden; }
        .rotate-y-180 { transform: rotateY(180deg); }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        /* 輕微晃動動畫 */
        @keyframes pulse-subtle {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        .pulse-effect { animation: pulse-subtle 2s infinite ease-in-out; }
    </style>
</head>
<body class="text-[#262626]">

    <div id="app" class="max-w-md mx-auto min-h-screen flex flex-col bg-white border-x border-gray-100 relative shadow-2xl">
        
        <!-- Top Nav -->
        <header class="sticky top-0 z-50 bg-white border-b border-gray-200 px-4 py-3 flex justify-between items-center">
            <h1 class="text-2xl font-bold tracking-tight italic" style="font-family: 'Brush Script MT', cursive, sans-serif;">VocabGram</h1>
            <div class="flex space-x-5 text-xl">
                <i class="far fa-heart cursor-pointer hover:text-red-500 transition"></i>
                <i class="far fa-paper-plane cursor-pointer hover:text-blue-500 transition"></i>
            </div>
        </header>

        <!-- Main Content -->
        <main id="main-content" class="flex-1 pb-20 overflow-y-auto no-scrollbar">
            <!-- 預設顯示學習頁面內容 -->
            <div class="px-4 py-2 flex items-center mt-2">
                <div class="w-8 h-8 ig-gradient rounded-full p-[2px]">
                    <div class="w-full h-full bg-white rounded-full flex items-center justify-center text-[10px] font-bold">VG</div>
                </div>
                <span class="ml-3 font-semibold text-sm">今日新詞：高效衝刺中</span>
            </div>
            
            <div class="w-full aspect-square p-4">
                <div class="relative w-full h-full cursor-pointer" onclick="document.getElementById('flashcard').classList.toggle('flipped')">
                    <div id="flashcard" class="card-inner w-full h-full relative">
                        <!-- 正面 -->
                        <div class="absolute w-full h-full bg-gray-50 rounded-3xl border border-gray-100 flex flex-col items-center justify-center backface-hidden shadow-sm">
                            <h2 class="text-5xl font-bold mb-3 tracking-tight">completion</h2>
                            <p class="text-gray-400 italic text-lg">[kəmˈpliːʃ(ə)n]</p>
                            <div class="mt-12 px-6 py-2 bg-blue-50 text-blue-500 rounded-full text-xs font-bold pulse-effect">
                                點擊卡片查看釋義
                            </div>
                        </div>
                        <!-- 反面 -->
                        <div class="absolute w-full h-full bg-white rounded-3xl border border-gray-100 flex flex-col items-center justify-center backface-hidden rotate-y-180 shadow-lg p-8 text-center">
                            <span class="text-xs font-bold text-gray-300 uppercase tracking-widest mb-4">Meaning</span>
                            <p class="text-2xl font-bold text-gray-800 mb-6">n. 完成; 結束</p>
                            <div class="w-8 h-1 bg-gray-100 mb-6"></div>
                            <p class="text-sm text-gray-500 italic leading-relaxed">"The advancements in task completion were significant."</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 操作按鈕 -->
            <div class="px-8 flex justify-between items-center mt-6">
                <button class="flex flex-col items-center text-gray-400 hover:text-red-500 transition">
                    <div class="w-12 h-12 border-2 border-gray-100 rounded-full flex items-center justify-center mb-1">
                        <i class="fas fa-times text-xl"></i>
                    </div>
                    <span class="text-[10px]">太簡單了</span>
                </button>
                
                <button class="bg-[#0095f6] hover:bg-blue-600 text-white px-12 py-3 rounded-2xl font-bold shadow-md transform active:scale-95 transition">
                    下一個單字
                </button>

                <button class="flex flex-col items-center text-gray-400 hover:text-orange-500 transition">
                    <div class="w-12 h-12 border-2 border-gray-100 rounded-full flex items-center justify-center mb-1">
                        <i class="fas fa-redo-alt text-lg"></i>
                    </div>
                    <span class="text-[10px]">還不熟</span>
                </button>
            </div>

            <!-- 進度條 -->
            <div class="px-8 mt-10">
                <div class="flex justify-between items-end mb-2">
                    <span class="text-xs font-bold text-gray-400 uppercase">Today's Progress</span>
                    <span class="text-xs font-bold text-blue-500">12 / 20</span>
                </div>
                <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                    <div class="bg-blue-500 h-full w-[60%] rounded-full shadow-[0_0_8px_rgba(59,130,246,0.5)]"></div>
                </div>
            </div>
        </main>

        <!-- Bottom Tab Bar -->
        <nav class="fixed bottom-0 max-w-md w-full bg-white border-t border-gray-100 flex justify-around items-center py-2 z-50">
            <div class="active-tab flex flex-col items-center p-2">
                <i class="fas fa-home text-xl"></i>
                <span class="text-[10px] mt-1 font-bold">學習</span>
            </div>
            <div class="text-gray-300 flex flex-col items-center p-2">
                <i class="fas fa-history text-xl"></i>
                <span class="text-[10px] mt-1">複習</span>
            </div>
            <div class="text-gray-300 flex flex-col items-center p-2">
                <i class="fas fa-bolt text-xl"></i>
                <span class="text-[10px] mt-1">挑戰</span>
            </div>
            <div class="text-gray-300 flex flex-col items-center p-2">
                <i class="fas fa-search text-xl"></i>
                <span class="text-[10px] mt-1">搜尋</span>
            </div>
        </nav>
    </div>

</body>
</html>