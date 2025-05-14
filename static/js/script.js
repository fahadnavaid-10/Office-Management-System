document.addEventListener("DOMContentLoaded", () => {
  // Stats Button Functionality
  const statsBtn = document.getElementById("statsBtn")
  const statsOverlay = document.getElementById("statsOverlay")
  const closeStats = document.getElementById("closeStats")

  if (statsBtn) {
    statsBtn.addEventListener("click", () => {
      statsOverlay.style.display = "flex"
      document.body.style.overflow = "hidden"

      // Animate stats items
      const statItems = document.querySelectorAll(".stat-item")
      statItems.forEach((item, index) => {
        setTimeout(() => {
          item.style.opacity = "1"
          item.style.transform = "translateY(0)"
        }, 100 * index)
      })
    })
  }

  if (closeStats) {
    closeStats.addEventListener("click", () => {
      statsOverlay.style.display = "none"
      document.body.style.overflow = "auto"
    })
  }

  // Close overlay when clicking outside the card
  if (statsOverlay) {
    statsOverlay.addEventListener("click", (e) => {
      if (e.target === statsOverlay) {
        statsOverlay.style.display = "none"
        document.body.style.overflow = "auto"
      }
    })
  }

  // Animate elements when they come into view
  const animateOnScroll = () => {
    const elements = document.querySelectorAll(".result-container, .search-container")

    elements.forEach((element) => {
      const elementPosition = element.getBoundingClientRect().top
      const screenPosition = window.innerHeight / 1.3

      if (elementPosition < screenPosition) {
        element.classList.add("animate")
      }
    })
  }

  window.addEventListener("scroll", animateOnScroll)
  animateOnScroll() // Run once on page load

  // Calendar navigation
  const prevMonthBtn = document.querySelector(".month-btn.prev")
  const nextMonthBtn = document.querySelector(".month-btn.next")

  if (prevMonthBtn && nextMonthBtn) {
    // This would be implemented with backend integration
    // For now, just a placeholder
    prevMonthBtn.addEventListener("click", () => {
      alert("Previous month would be loaded from the backend")
    })

    nextMonthBtn.addEventListener("click", () => {
      alert("Next month would be loaded from the backend")
    })
  }

  // Form validation for Add Employee
  const employeeForm = document.getElementById("employeeForm")
  if (employeeForm) {
    employeeForm.addEventListener("submit", (e) => {
      let valid = true
      const name = document.getElementById("name").value.trim()
      const address = document.getElementById("address").value.trim()
      const phone = document.getElementById("phone").value.trim()
      const departmentId = document.getElementById("department_id").value.trim()
      const managerId = document.getElementById("manager_id").value.trim()

      if (!name || !address || !phone || !departmentId || !managerId) {
        valid = false
        alert("All fields are required!")
      }

      if (!valid) {
        e.preventDefault()
      }
    })
  }

  // Form validation for Add Department
  const departmentForm = document.getElementById("departmentForm")
  if (departmentForm) {
    departmentForm.addEventListener("submit", (e) => {
      let valid = true
      const name = document.getElementById("name").value.trim()
      const area = document.getElementById("area").value.trim()

      if (!name || !area) {
        valid = false
        alert("All fields are required!")
      }

      if (!valid) {
        e.preventDefault()
      }
    })
  }
})
