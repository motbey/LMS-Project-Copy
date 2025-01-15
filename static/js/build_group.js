// Initialize data when the DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM Content Loaded"); // Debug log

  try {
    // Initialize rules array first
    window.rules = [];

    // Get the initial data from the script tag
    const initialDataElement = document.getElementById("initialData");
    console.log("Initial Data Element:", initialDataElement); // Debug log

    if (!initialDataElement) {
      console.error("Initial data element not found!");
      return;
    }

    const initialData = JSON.parse(initialDataElement.textContent);
    console.log("Parsed Initial Data:", initialData); // Debug log

    // Set up global data
    window.serverData = {
      roles: initialData.roles || [],
      companies: initialData.companies || [],
      jobTitles: initialData.jobTitles || [],
      locations: initialData.locations || [],
    };
    console.log("Server Data:", window.serverData); // Debug log

    // Initialize rules if they exist in initial data
    if (initialData.existingCriteria) {
      window.rules = initialData.existingCriteria.map((criteria) => {
        // Get the actual name based on the ID and type
        let displayName = criteria.text;
        switch (criteria.type) {
          case "company":
            const company = serverData.companies.find(
              (c) => c.id.toString() === criteria.value
            );
            displayName = company ? company.name : criteria.value;
            break;
          case "location":
            const location = serverData.locations.find(
              (l) => l.id.toString() === criteria.value
            );
            displayName = location ? location.name : criteria.value;
            break;
          case "job_title":
            const jobTitle = serverData.jobTitles.find(
              (j) => j.id.toString() === criteria.value
            );
            displayName = jobTitle ? jobTitle.name : criteria.value;
            break;
          case "role":
            displayName = criteria.value; // Roles are already text values
            break;
        }

        // Format the display text
        let displayText;
        switch (criteria.type) {
          case "company":
            displayText = `Company: ${displayName}`;
            break;
          case "location":
            displayText = `Location: ${displayName}`;
            break;
          case "job_title":
            displayText = `Job Title: ${displayName}`;
            break;
          case "role":
            displayText = `Role: ${displayName}`;
            break;
          default:
            displayText = `${criteria.type}: ${displayName}`;
        }

        return {
          type: criteria.type,
          value: criteria.value,
          text: displayText,
        };
      });
    }

    // Set up event listeners
    const ruleTypeSelect = document.getElementById("ruleTypeSelect");
    console.log("Rule Type Select Element:", ruleTypeSelect); // Debug log

    if (!ruleTypeSelect) {
      console.error("Rule type select element not found!");
      return;
    }

    ruleTypeSelect.addEventListener("change", function () {
      console.log("Rule type changed to:", this.value); // Debug log
      const type = this.value;
      const conditionsDiv = document.getElementById("ruleConditions");
      const conditionSelect = document.getElementById("conditionSelect");
      const addRuleBtn = document.getElementById("addRuleBtn");

      if (!type) {
        conditionsDiv.style.display = "none";
        addRuleBtn.style.display = "none";
        return;
      }

      // Show the conditions div and button
      conditionsDiv.style.display = "block";
      addRuleBtn.style.display = "block";

      // Clear and populate the conditions dropdown
      conditionSelect.innerHTML =
        '<option value="">Select a condition...</option>';

      switch (type) {
        case "role":
          serverData.roles.forEach((role) =>
            conditionSelect.add(new Option(role, role))
          );
          break;
        case "company":
          serverData.companies.forEach((company) =>
            conditionSelect.add(new Option(company.name, company.id))
          );
          break;
        case "job_title":
          serverData.jobTitles.forEach((jobTitle) =>
            conditionSelect.add(new Option(jobTitle.name, jobTitle.id))
          );
          break;
        case "location":
          serverData.locations.forEach((location) =>
            conditionSelect.add(new Option(location.name, location.id))
          );
          break;
      }
    });

    // Add rule button event listener
    const addRuleBtn = document.getElementById("addRuleBtn");
    addRuleBtn.addEventListener("click", function () {
      const type = document.getElementById("ruleTypeSelect").value;
      const select = document.getElementById("conditionSelect");
      const value = select.value;
      const text = select.options[select.selectedIndex].text;

      if (!type || !value) {
        showMessage("Please select both a rule type and condition.", "warning");
        return;
      }

      // Format the display text based on the type
      let displayText;
      switch (type) {
        case "company":
          displayText = `Company: ${text}`;
          break;
        case "location":
          displayText = `Location: ${text}`;
          break;
        case "job_title":
          displayText = `Job Title: ${text}`;
          break;
        case "role":
          displayText = `Role: ${text}`;
          break;
        default:
          displayText = `${type}: ${text}`;
      }

      // Check for duplicate rules
      const isDuplicate = window.rules.some(
        (rule) => rule.type === type && rule.value === value
      );

      if (isDuplicate) {
        showMessage("This rule already exists.", "warning");
        return;
      }

      window.rules.push({ type, value, text: displayText });
      showMessage("Rule added successfully!", "success");
      updateRulesList();

      // Reset selections
      document.getElementById("ruleTypeSelect").value = "";
      document.getElementById("ruleConditions").style.display = "none";
      document.getElementById("addRuleBtn").style.display = "none";
    });

    // Initialize the rules list
    updateRulesList();
  } catch (error) {
    console.error("Error initializing group builder:", error);
  }
});

function updateRulesList() {
  const rulesList = document.getElementById("rulesList");
  const preview = document.getElementById("rulePreview");

  if (!window.rules || window.rules.length === 0) {
    rulesList.innerHTML = "<p>No rules added yet.</p>";
    preview.textContent = "No rules configured yet.";
  } else {
    const rulesHtml = window.rules
      .map(
        (rule, i) =>
          `<div class="rule-item">
                <span>${rule.text}</span>
                <button type="button" onclick="deleteRule(${i})">×</button>
            </div>`
      )
      .join("");

    rulesList.innerHTML = rulesHtml;

    // Format the preview text using the same format as the rules
    const previewText = window.rules
      .map((rule) => {
        // Use the formatted text that was created when adding the rule
        return rule.text;
      })
      .join(" AND ");

    preview.textContent = previewText;
  }

  document.getElementById("savedRules").value = JSON.stringify(window.rules);
}

function deleteRule(index) {
  if (confirm("Are you sure you want to delete this rule?")) {
    window.rules.splice(index, 1);
    updateRulesList();
    showMessage("Rule deleted successfully!", "success");
  }
}

function showMessage(message, type = "info") {
  const messageDiv = document.createElement("div");
  messageDiv.className = `alert alert-${type} alert-dismissible fade show`;
  messageDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

  // Insert at the top of the container
  const container = document.querySelector(".container");
  container.insertBefore(messageDiv, container.firstChild);

  // Auto dismiss after 5 seconds
  setTimeout(() => {
    messageDiv.remove();
  }, 5000);
}

// Add form submission validation
document.getElementById("rulesForm").addEventListener("submit", function (e) {
  if (window.rules.length === 0) {
    e.preventDefault();
    showMessage("Please add at least one rule before saving.", "warning");
  }
});
