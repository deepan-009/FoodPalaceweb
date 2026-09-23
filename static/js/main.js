/* Food Palace — interaction layer.
   Everything degrades gracefully: with JS off you still get the full menu,
   all reviews and a working contact form. */

(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Sticky header + mobile nav --------------------------------- */
  var masthead = document.querySelector(".masthead");
  var nav = document.querySelector(".nav");
  var toggle = document.querySelector(".nav-toggle");

  if (masthead) {
    var onScroll = function () {
      masthead.classList.toggle("is-stuck", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- Scroll reveal ---------------------------------------------- */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && !reduced && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -60px" }
    );
    reveals.forEach(function (el) {
      io.observe(el);
    });
  } else {
    reveals.forEach(function (el) {
      el.classList.add("is-in");
    });
  }

  /* ---------- Live open / closed ----------------------------------------- */
  // The kitchen runs 6:00 am to 11:30 pm, seven days, Asia/Kolkata.
  function refreshStatus() {
    var pills = document.querySelectorAll("[data-status]");
    if (!pills.length) return;

    var nowIST = new Date(
      new Date().toLocaleString("en-US", { timeZone: "Asia/Kolkata" })
    );
    var minutes = nowIST.getHours() * 60 + nowIST.getMinutes();
    var open = minutes >= 360 && minutes < 1410; // 06:00 -> 23:30

    var label;
    if (open) {
      var left = 1410 - minutes;
      label =
        left <= 60
          ? "Closing in " + left + " min"
          : "Open now · till 11:30 pm";
    } else {
      label = minutes < 360 ? "Opens at 6 am" : "Closed · opens 6 am";
    }

    pills.forEach(function (pill) {
      pill.classList.toggle("is-open", open);
      var text = pill.querySelector("[data-status-text]");
      if (text) text.textContent = label;
    });
  }
  refreshStatus();
  setInterval(refreshStatus, 60000);

  // Highlight today's row in the hours table.
  var todayRow = document.querySelector(
    '[data-day="' +
      new Date()
        .toLocaleString("en-US", { timeZone: "Asia/Kolkata", weekday: "long" })
        .toLowerCase() +
      '"]'
  );
  if (todayRow) todayRow.classList.add("is-today");

  /* ---------- Menu search + diet filter ---------------------------------- */
  var search = document.getElementById("menu-search");
  var dietBtns = document.querySelectorAll("[data-diet]");
  var emptyNote = document.getElementById("menu-empty");
  var diet = "all";

  function applyMenuFilters() {
    if (!document.querySelector(".menu-row")) return;
    var term = (search ? search.value : "").trim().toLowerCase();
    var visible = 0;

    document.querySelectorAll(".menu-cat").forEach(function (cat) {
      var shown = 0;
      cat.querySelectorAll(".menu-row").forEach(function (row) {
        var name = (row.dataset.name || "").toLowerCase();
        var isVeg = row.dataset.veg === "1";
        var matchesTerm = !term || name.indexOf(term) !== -1;
        var matchesDiet =
          diet === "all" || (diet === "veg" ? isVeg : !isVeg);
        var show = matchesTerm && matchesDiet;
        row.hidden = !show;
        if (show) shown++;
      });
      cat.hidden = shown === 0;
      visible += shown;
    });

    document.querySelectorAll(".menu-kitchen").forEach(function (block) {
      var any = block.querySelector(".menu-cat:not([hidden])");
      block.hidden = !any;
    });

    if (emptyNote) emptyNote.hidden = visible !== 0;
  }

  if (search) {
    var t;
    search.addEventListener("input", function () {
      clearTimeout(t);
      t = setTimeout(applyMenuFilters, 120);
    });
    search.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        search.value = "";
        applyMenuFilters();
      }
    });
  }

  dietBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      dietBtns.forEach(function (b) {
        b.classList.remove("is-on");
        b.setAttribute("aria-pressed", "false");
      });
      btn.classList.add("is-on");
      btn.setAttribute("aria-pressed", "true");
      diet = btn.dataset.diet;
      applyMenuFilters();
    });
  });

  /* ---------- Rating bars animate on reveal ------------------------------ */
  var bars = document.querySelectorAll(".bar span[data-pct]");
  if (bars.length) {
    var fill = function () {
      bars.forEach(function (bar) {
        bar.style.width = bar.dataset.pct + "%";
      });
    };
    if ("IntersectionObserver" in window && !reduced) {
      var bio = new IntersectionObserver(
        function (entries) {
          if (entries.some(function (e) { return e.isIntersecting; })) {
            fill();
            bio.disconnect();
          }
        },
        { threshold: 0.3 }
      );
      bio.observe(bars[0].closest(".rating-panel") || bars[0]);
    } else {
      fill();
    }
  }

  /* ---------- Toast ------------------------------------------------------ */
  var toast = document.getElementById("toast");
  var toastTimer;
  function say(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("is-up");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toast.classList.remove("is-up");
    }, 2600);
  }

  function csrfToken() {
    var field = document.querySelector("[name=csrfmiddlewaretoken]");
    if (field) return field.value;
    var match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : "";
  }

  /* ---------- Review card interactions ----------------------------------- */
  document.addEventListener("click", function (event) {
    // Three-dot menu
    var dots = event.target.closest("[data-menu-toggle]");
    document.querySelectorAll(".review__dropdown.is-open").forEach(function (d) {
      if (!dots || d !== dots.parentElement.querySelector(".review__dropdown")) {
        d.classList.remove("is-open");
      }
    });
    if (dots) {
      var dd = dots.parentElement.querySelector(".review__dropdown");
      if (dd) {
        var open = dd.classList.toggle("is-open");
        dots.setAttribute("aria-expanded", open ? "true" : "false");
      }
      return;
    }

    // Like
    var like = event.target.closest("[data-like]");
    if (like) {
      var card = like.closest(".review");
      var count = like.querySelector(".act__count");
      var url = like.dataset.like;

      // Optimistic update so the tap feels instant.
      var wasLiked = like.classList.contains("is-liked");
      like.classList.toggle("is-liked", !wasLiked);
      if (count) {
        count.textContent = Math.max(0, parseInt(count.textContent || "0", 10) + (wasLiked ? -1 : 1));
      }

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken(),
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r); })
        .then(function (data) {
          like.classList.toggle("is-liked", data.liked);
          if (count) count.textContent = data.likes;
        })
        .catch(function () {
          // Roll back if the server did not take it.
          like.classList.toggle("is-liked", wasLiked);
          if (count) {
            count.textContent = Math.max(0, parseInt(count.textContent || "0", 10) + (wasLiked ? 1 : -1));
          }
          say("Could not save that like");
        });
      return;
    }

    // Share
    var share = event.target.closest("[data-share]");
    if (share) {
      var reviewCard = share.closest(".review");
      var author = reviewCard.querySelector(".review__name");
      var body = reviewCard.querySelector(".review__text");
      var payload = {
        title: "Review of Food Palace Family Restaurant",
        text:
          (author ? author.textContent.trim() + ": " : "") +
          (body ? body.textContent.trim().slice(0, 180) : ""),
        url: window.location.origin + window.location.pathname + "#review-" + (reviewCard.dataset.id || ""),
      };
      if (navigator.share) {
        navigator.share(payload).catch(function () {});
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(payload.text + " — " + payload.url).then(function () {
          say("Review copied to clipboard");
        });
      } else {
        say("Copy the link from your address bar");
      }
      return;
    }

    // Dropdown items
    var action = event.target.closest("[data-review-action]");
    if (action) {
      var kind = action.dataset.reviewAction;
      if (kind === "copy") {
        var txt = action.closest(".review").querySelector(".review__text");
        if (navigator.clipboard && txt) {
          navigator.clipboard.writeText(txt.textContent.trim());
          say("Review text copied");
        }
      } else if (kind === "report") {
        say("Thanks, we will take a look");
      } else if (kind === "google") {
        window.open(action.dataset.url || "#", "_blank", "noopener");
      }
      action.closest(".review__dropdown").classList.remove("is-open");
      return;
    }

    // Read more / less
    var more = event.target.closest(".review__more");
    if (more) {
      var para = more.previousElementSibling;
      var clamped = para.classList.toggle("is-clamped");
      more.textContent = clamped ? "Read more" : "Show less";
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll(".review__dropdown.is-open").forEach(function (d) {
        d.classList.remove("is-open");
      });
    }
  });

  /* Clamp only the long reviews. Apply the clamp first, then measure: an
     unclamped paragraph never reports overflow. */
  function setUpClamps() {
    document.querySelectorAll(".review__text:not([data-checked])").forEach(function (para) {
      para.dataset.checked = "1";
      para.classList.add("is-clamped");
      if (para.scrollHeight <= para.clientHeight + 4) {
        para.classList.remove("is-clamped");
        return;
      }
      var btn = document.createElement("button");
      btn.className = "review__more";
      btn.type = "button";
      btn.textContent = "Read more";
      para.insertAdjacentElement("afterend", btn);
    });
  }

  setUpClamps();
  // Web fonts change the line count, so re-measure once they land.
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () {
      document.querySelectorAll(".review__text").forEach(function (para) {
        if (!para.nextElementSibling || !para.nextElementSibling.classList.contains("review__more")) {
          delete para.dataset.checked;
          para.classList.remove("is-clamped");
        }
      });
      setUpClamps();
    });
  }

  /* ---------- Hero parallax (desktop, motion allowed) -------------------- */
  var hero = document.querySelector("[data-parallax]");
  if (hero && !reduced && window.innerWidth > 900) {
    window.addEventListener(
      "scroll",
      function () {
        var y = window.scrollY;
        if (y < 700) hero.style.transform = "translateY(" + y * 0.08 + "px)";
      },
      { passive: true }
    );
  }
})();
