/**
 * AI Video Studio Frontend Controller.
 * Handles drag-and-drop, AI script generation, voice preview, video rendering, and history.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const tabVideo = document.getElementById("tabVideo");
  const tabSample = document.getElementById("tabSample");
  const tabImages = document.getElementById("tabImages");

  const videoUploadSection = document.getElementById("videoUploadSection");
  const sampleVideoSection = document.getElementById("sampleVideoSection");
  const imagesUploadSection = document.getElementById("imagesUploadSection");

  const videoDropzone = document.getElementById("videoDropzone");
  const videoFileInput = document.getElementById("videoFileInput");
  const videoFileList = document.getElementById("videoFileList");

  const imagesDropzone = document.getElementById("imagesDropzone");
  const imagesFileInput = document.getElementById("imagesFileInput");
  const imagesFileList = document.getElementById("imagesFileList");

  const aspectRatioSelect = document.getElementById("aspectRatioSelect");
  const topicInput = document.getElementById("topicInput");
  const btnAiGenerate = document.getElementById("btnAiGenerate");
  const btnFillSampleScript = document.getElementById("btnFillSampleScript");
  const btnAiPolish = document.getElementById("btnAiPolish");
  const scriptText = document.getElementById("scriptText");

  const voiceTypeSelect = document.getElementById("voiceTypeSelect");
  const speedSlider = document.getElementById("speedSlider");
  const speedDisplay = document.getElementById("speedDisplay");
  const btnPreviewVoice = document.getElementById("btnPreviewVoice");
  const previewAudioPlayer = document.getElementById("previewAudioPlayer");

  const chkWithBgm = document.getElementById("chkWithBgm");
  const bgmControlsRow = document.getElementById("bgmControlsRow");
  const bgmTrackSelect = document.getElementById("bgmTrackSelect");
  const bgmVolumeSlider = document.getElementById("bgmVolumeSlider");
  const bgmVolumeDisplay = document.getElementById("bgmVolumeDisplay");

  const btnRenderVideo = document.getElementById("btnRenderVideo");
  const playerPlaceholder = document.getElementById("playerPlaceholder");
  const finalVideoPlayer = document.getElementById("finalVideoPlayer");
  const progressBox = document.getElementById("progressBox");
  const progressStatusText = document.getElementById("progressStatusText");
  const progressPercent = document.getElementById("progressPercent");
  const progressBarFill = document.getElementById("progressBarFill");
  const downloadActionRow = document.getElementById("downloadActionRow");
  const btnDownloadVideo = document.getElementById("btnDownloadVideo");
  const videoTimeTag = document.getElementById("videoTimeTag");
  const historyList = document.getElementById("historyList");
  const btnRefreshHistory = document.getElementById("btnRefreshHistory");

  // API Modal elements
  const btnOpenApiModal = document.getElementById("btnOpenApiModal");
  const btnCloseApiModal = document.getElementById("btnCloseApiModal");
  const btnCancelModal = document.getElementById("btnCancelModal");
  const btnSaveApiConfig = document.getElementById("btnSaveApiConfig");
  const apiModal = document.getElementById("apiModal");
  const modalApiProvider = document.getElementById("modalApiProvider");
  const modalKeyGroup = document.getElementById("modalKeyGroup");
  const modalApiKeyInput = document.getElementById("modalApiKeyInput");
  const apiStatusText = document.getElementById("apiStatusText");
  const currentAiBadge = document.getElementById("currentAiBadge");

  // App State
  let currentMediaType = "video"; // "video", "sample", "images"
  let selectedVideoFile = null;
  let selectedImageFiles = [];

  // Sample script from user prompt
  const SAMPLE_HAIR_SCRIPT = "Tóc móc tay từ tóc thật 100%, tự nhiên như tóc mọc từ chân tóc luôn nha mọi người. Hiện tại bên mình có sẵn rất nhiều dáng từ tóc ngắn, tóc dài, uốn xoăn cho đến các màu nhuộm highlight cực xinh. Mọi người ưng mẫu nào thì cứ bấm thẳng vào giỏ hàng màn hình để chọn nha. Còn chị em nào muốn đặt thiết kế riêng theo độ dài, kiểu mái hoặc màu sắc yêu thích thì cứ nhắn tin trực tiếp cho mình mình làm theo yêu cầu nha.";

  // 1. Initial Config from LocalStorage
  let apiConfig = {
    provider: localStorage.getItem("ai_provider") || "offline",
    apiKey: localStorage.getItem("ai_api_key") || ""
  };
  updateApiStatusUI();

  // 2. Tab Navigation
  function switchTab(type) {
    currentMediaType = type;
    [tabVideo, tabSample, tabImages].forEach(t => t.classList.remove("active"));
    videoUploadSection.style.display = "none";
    sampleVideoSection.style.display = "none";
    imagesUploadSection.style.display = "none";

    if (type === "video") {
      tabVideo.classList.add("active");
      videoUploadSection.style.display = "block";
    } else if (type === "sample") {
      tabSample.classList.add("active");
      sampleVideoSection.style.display = "block";
    } else if (type === "images") {
      tabImages.classList.add("active");
      imagesUploadSection.style.display = "block";
    }
  }

  tabVideo.addEventListener("click", () => switchTab("video"));
  tabSample.addEventListener("click", () => switchTab("sample"));
  tabImages.addEventListener("click", () => switchTab("images"));

  // 3. Drag & Drop for Video
  videoDropzone.addEventListener("click", () => videoFileInput.click());
  videoDropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    videoDropzone.classList.add("dragover");
  });
  videoDropzone.addEventListener("dragleave", () => videoDropzone.classList.remove("dragover"));
  videoDropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    videoDropzone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleVideoFile(e.dataTransfer.files[0]);
    }
  });
  videoFileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      handleVideoFile(e.target.files[0]);
    }
  });

  function handleVideoFile(file) {
    selectedVideoFile = file;
    const szMB = (file.size / (1024 * 1024)).toFixed(1);
    videoFileList.innerHTML = `
      <div class="file-tag">
        🎥 <strong>${file.name}</strong> (${szMB} MB)
        <span style="cursor: pointer; color: red; margin-left: 6px;" onclick="removeVideoFile()">✕</span>
      </div>
    `;
  }

  window.removeVideoFile = function() {
    selectedVideoFile = null;
    videoFileInput.value = "";
    videoFileList.innerHTML = "";
  };

  // 4. Drag & Drop for Images
  imagesDropzone.addEventListener("click", () => imagesFileInput.click());
  imagesDropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    imagesDropzone.classList.add("dragover");
  });
  imagesDropzone.addEventListener("dragleave", () => imagesDropzone.classList.remove("dragover"));
  imagesDropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    imagesDropzone.classList.remove("dragover");
    if (e.dataTransfer.files) {
      handleImageFiles(Array.from(e.dataTransfer.files));
    }
  });
  imagesFileInput.addEventListener("change", (e) => {
    if (e.target.files) {
      handleImageFiles(Array.from(e.target.files));
    }
  });

  function handleImageFiles(files) {
    selectedImageFiles = files.filter(f => f.type.startsWith("image/"));
    renderImageList();
  }

  function renderImageList() {
    if (selectedImageFiles.length === 0) {
      imagesFileList.innerHTML = "";
      return;
    }
    imagesFileList.innerHTML = selectedImageFiles.map((f, i) => `
      <div class="file-tag">
        🖼 ${f.name}
        <span style="cursor: pointer; color: red; margin-left: 4px;" onclick="removeImageFile(${i})">✕</span>
      </div>
    `).join("");
  }

  window.removeImageFile = function(idx) {
    selectedImageFiles.splice(idx, 1);
    renderImageList();
  };

  // 5. Script Actions
  btnFillSampleScript.addEventListener("click", () => {
    scriptText.value = SAMPLE_HAIR_SCRIPT;
    topicInput.value = "Tóc móc tay từ tóc thật 100%";
    switchTab("sample");
  });

  // Call AI Script Generator
  btnAiGenerate.addEventListener("click", async () => {
    const topic = topicInput.value.trim() || "Sản phẩm thời trang cao cấp";
    btnAiGenerate.disabled = true;
    btnAiGenerate.textContent = "⏳ Đang viết...";

    try {
      const res = await fetch("/api/generate-script", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: topic,
          tone: "humorous",
          duration: 30,
          api_provider: apiConfig.provider,
          api_key: apiConfig.apiKey
        })
      });
      const data = await res.json();
      if (data.status === "success" && data.script) {
        scriptText.value = data.script;
      } else {
        alert("Không thể tạo kịch bản: " + (data.detail || "Lỗi server"));
      }
    } catch (e) {
      alert("Lỗi kết nối tới AI API: " + e.message);
    } finally {
      btnAiGenerate.disabled = false;
      btnAiGenerate.textContent = "✨ Viết Bằng AI";
    }
  });

  // Polish script humor
  btnAiPolish.addEventListener("click", async () => {
    const text = scriptText.value.trim();
    if (!text) {
      alert("Vui lòng nhập hoặc viết một đoạn kịch bản trước khi tút lại!");
      return;
    }
    btnAiPolish.disabled = true;
    btnAiPolish.textContent = "⏳ Đang tút lại...";

    try {
      const res = await fetch("/api/polish-script", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          script: text,
          api_provider: apiConfig.provider,
          api_key: apiConfig.apiKey
        })
      });
      const data = await res.json();
      if (data.status === "success" && data.script) {
        scriptText.value = data.script;
      }
    } catch (e) {
      alert("Lỗi tút lại kịch bản: " + e.message);
    } finally {
      btnAiPolish.disabled = false;
      btnAiPolish.textContent = "🎭 Tút Lại Hài Hước Hơn";
    }
  });

  // 6. Voice & Speed Controls
  speedSlider.addEventListener("input", () => {
    speedDisplay.textContent = `${parseFloat(speedSlider.value).toFixed(2)}x`;
  });

  chkWithBgm.addEventListener("change", () => {
    bgmControlsRow.style.display = chkWithBgm.checked ? "grid" : "none";
  });

  bgmVolumeSlider.addEventListener("input", () => {
    bgmVolumeDisplay.textContent = `${Math.round(bgmVolumeSlider.value * 100)}%`;
  });

  // Voice Preview
  btnPreviewVoice.addEventListener("click", async () => {
    const text = scriptText.value.trim() || SAMPLE_HAIR_SCRIPT;
    btnPreviewVoice.disabled = true;
    btnPreviewVoice.textContent = "⏳ Đang tạo audio...";

    try {
      const res = await fetch("/api/preview-voice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: text,
          voice_type: voiceTypeSelect.value,
          speed: parseFloat(speedSlider.value),
          pitch_style: voiceTypeSelect.value.includes("hai_huoc") ? "playful" : "natural"
        })
      });
      const data = await res.json();
      if (data.status === "success" && data.audio_url) {
        previewAudioPlayer.src = data.audio_url;
        previewAudioPlayer.style.display = "block";
        previewAudioPlayer.play();
      } else {
        alert("Lỗi tạo voice: " + (data.detail || "Không rõ"));
      }
    } catch (e) {
      alert("Lỗi kết nối: " + e.message);
    } finally {
      btnPreviewVoice.disabled = false;
      btnPreviewVoice.textContent = "🔊 Nghe thử giọng đọc trước";
    }
  });

  // 7. Render Final Video
  btnRenderVideo.addEventListener("click", async () => {
    const script = scriptText.value.trim();
    if (!script) {
      alert("Vui lòng nhập lời đọc lồng tiếng (Voice-over) trước khi tạo video!");
      scriptText.focus();
      return;
    }

    if (currentMediaType === "video" && !selectedVideoFile) {
      alert("Vui lòng tải lên 1 file video, hoặc chuyển sang tab 'Video Mẫu'!");
      return;
    }

    if (currentMediaType === "images" && selectedImageFiles.length === 0) {
      alert("Vui lòng chọn ít nhất 1 hình ảnh để tạo slideshow!");
      return;
    }

    // Build form data
    const formData = new FormData();
    formData.append("script_text", script);
    formData.append("voice_type", voiceTypeSelect.value);
    formData.append("speed", speedSlider.value);
    formData.append("pitch_style", voiceTypeSelect.value.includes("hai_huoc") ? "playful" : "natural");
    formData.append("with_bgm", chkWithBgm.checked);
    formData.append("bgm_name", bgmTrackSelect.value);
    formData.append("bgm_volume", bgmVolumeSlider.value);
    formData.append("aspect_ratio", aspectRatioSelect.value);

    if (currentMediaType === "sample") {
      formData.append("media_type", "video");
      formData.append("use_sample_video", "true");
    } else if (currentMediaType === "video") {
      formData.append("media_type", "video");
      formData.append("use_sample_video", "false");
      formData.append("video_file", selectedVideoFile);
    } else if (currentMediaType === "images") {
      formData.append("media_type", "images");
      for (const img of selectedImageFiles) {
        formData.append("image_files", img);
      }
    }

    // UI Progress State
    btnRenderVideo.disabled = true;
    btnRenderVideo.textContent = "⏳ ĐANG XỬ LÝ & RENDER VIDEO...";
    progressBox.style.display = "block";
    updateProgress(15, "Đang tổng hợp giọng nói AI...");

    // Simulated progress ticker
    const timer = setInterval(() => {
      let cur = parseInt(progressBarFill.style.width) || 15;
      if (cur < 85) {
        cur += 5;
        let msg = "Đang xử lý hình ảnh & loop video...";
        if (cur > 50) msg = "Đang mix nhạc nền & đồng bộ âm thanh...";
        if (cur > 75) msg = "Đang xuất bản file video độ nét cao...";
        updateProgress(cur, msg);
      }
    }, 1200);

    try {
      const res = await fetch("/api/render-video", {
        method: "POST",
        body: formData
      });
      clearInterval(timer);

      const data = await res.json();
      if (data.status === "success" && data.video_url) {
        updateProgress(100, "Render hoàn tất 100%!");
        
        // Show in player
        playerPlaceholder.style.display = "none";
        finalVideoPlayer.style.display = "block";
        finalVideoPlayer.src = data.video_url;
        finalVideoPlayer.load();
        finalVideoPlayer.play();

        // Download button
        btnDownloadVideo.href = data.video_url;
        btnDownloadVideo.download = data.filename;
        downloadActionRow.style.display = "block";

        videoTimeTag.textContent = `${data.duration}s (${data.size_mb} MB)`;
        videoTimeTag.style.display = "inline-block";

        loadHistory();
      } else {
        alert("Lỗi khi render video: " + (data.detail || "Không rõ nguyên nhân"));
      }
    } catch (e) {
      clearInterval(timer);
      alert("Lỗi kết nối tới server: " + e.message);
    } finally {
      btnRenderVideo.disabled = false;
      btnRenderVideo.textContent = "⚡ TẠO VIDEO HOÀN CHỈNH NGAY";
      setTimeout(() => {
        progressBox.style.display = "none";
      }, 3500);
    }
  });

  function updateProgress(pct, statusText) {
    progressBarFill.style.width = `${pct}%`;
    progressPercent.textContent = `${pct}%`;
    progressStatusText.textContent = statusText;
  }

  // 8. History Management
  async function loadHistory() {
    try {
      const res = await fetch("/api/history");
      const data = await res.json();
      if (data.history && data.history.length > 0) {
        historyList.innerHTML = data.history.map(item => `
          <div class="history-item">
            <div>
              <div class="history-name">${item.filename}</div>
              <div class="history-meta">${item.time} • ${item.size_mb} MB</div>
            </div>
            <div style="display: flex; gap: 6px;">
              <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 11px;" onclick="playHistoryVideo('${item.url}')">Xem</button>
              <a href="${item.url}" download="${item.filename}" class="btn btn-primary" style="padding: 4px 10px; font-size: 11px;">Tải</a>
            </div>
          </div>
        `).join("");
      } else {
        historyList.innerHTML = `<div style="text-align: center; color: var(--slate-gray); font-size: 13px; padding: 12px;">Chưa có video nào được tạo.</div>`;
      }
    } catch (e) {
      console.log("Error loading history:", e);
    }
  }

  window.playHistoryVideo = function(url) {
    playerPlaceholder.style.display = "none";
    finalVideoPlayer.style.display = "block";
    finalVideoPlayer.src = url;
    finalVideoPlayer.load();
    finalVideoPlayer.play();
    btnDownloadVideo.href = url;
    downloadActionRow.style.display = "block";
  };

  btnRefreshHistory.addEventListener("click", loadHistory);
  loadHistory();

  // 9. API Modal Management
  btnOpenApiModal.addEventListener("click", () => {
    modalApiProvider.value = apiConfig.provider;
    modalApiKeyInput.value = apiConfig.apiKey;
    modalKeyGroup.style.display = apiConfig.provider === "offline" ? "none" : "block";
    apiModal.style.display = "flex";
  });

  function closeModal() {
    apiModal.style.display = "none";
  }

  btnCloseApiModal.addEventListener("click", closeModal);
  btnCancelModal.addEventListener("click", closeModal);

  modalApiProvider.addEventListener("change", () => {
    modalKeyGroup.style.display = modalApiProvider.value === "offline" ? "none" : "block";
  });

  btnSaveApiConfig.addEventListener("click", () => {
    apiConfig.provider = modalApiProvider.value;
    apiConfig.apiKey = modalApiKeyInput.value.trim();

    localStorage.setItem("ai_provider", apiConfig.provider);
    localStorage.setItem("ai_api_key", apiConfig.apiKey);

    updateApiStatusUI();
    closeModal();
  });

  function updateApiStatusUI() {
    if (apiConfig.provider === "gemini") {
      apiStatusText.textContent = apiConfig.apiKey ? "AI: Google Gemini API (Sẵn sàng)" : "AI: Gemini (Chưa nhập Key)";
      currentAiBadge.textContent = "Google Gemini";
    } else if (apiConfig.provider === "openai") {
      apiStatusText.textContent = apiConfig.apiKey ? "AI: OpenAI GPT-4o (Sẵn sàng)" : "AI: OpenAI (Chưa nhập Key)";
      currentAiBadge.textContent = "OpenAI GPT-4o";
    } else {
      apiStatusText.textContent = "AI: Tích hợp sẵn (Sẵn sàng)";
      currentAiBadge.textContent = "AI Tích hợp";
    }
  }
});
