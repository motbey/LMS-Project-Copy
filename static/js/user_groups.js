function showModal() {
  document.getElementById("modalOverlay").classList.add("show");
  document.getElementById("modalContainer").classList.add("show");
}

function hideModal() {
  document.getElementById("modalOverlay").classList.remove("show");
  document.getElementById("modalContainer").classList.remove("show");
  document.getElementById("modalTitle").textContent = "Create New Group";
  document.getElementById("groupForm").action = "/create_group";
  document.getElementById("groupForm").reset();
  document.getElementById("groupId").value = "";
}

function editGroup(id, name, description) {
  document.getElementById("modalTitle").textContent = "Edit Group";
  document.getElementById("name").value = name;
  document.getElementById("description").value = description;
  document.getElementById("groupId").value = id;
  document.getElementById("groupForm").action = `/edit_group/${id}`;
  showModal();
}

function toggleDropdown(event, groupId) {
  console.log("Toggle dropdown called for group:", groupId);
  event.preventDefault();
  event.stopPropagation();

  const dropdown = document.getElementById(`dropdown-${groupId}`);
  console.log("Found dropdown element:", dropdown);

  document.querySelectorAll(".dropdown-content").forEach((d) => {
    if (d.id !== `dropdown-${groupId}`) {
      d.classList.remove("show");
    }
  });

  console.log(
    "Before toggle - has show class:",
    dropdown.classList.contains("show")
  );
  dropdown.classList.toggle("show");
  console.log(
    "After toggle - has show class:",
    dropdown.classList.contains("show")
  );
}

// Close dropdowns when clicking outside
document.addEventListener("click", function (event) {
  if (!event.target.closest(".dropdown")) {
    document.querySelectorAll(".dropdown-content").forEach((dropdown) => {
      dropdown.classList.remove("show");
    });
  }
});

// Close modal when clicking outside
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("modalOverlay").addEventListener("click", hideModal);
});

function editGroupFromData(button) {
  const id = button.dataset.id;
  const name = button.dataset.name;
  const description = button.dataset.description;
  editGroup(id, name, description);
}
