// Add Contact
document
  .getElementById("addContactForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
      const response = await fetch("/point-of-contact/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (response.ok) {
        // Generate styled popup
        const popup = document.createElement("div");
        popup.classList.add("popup");

        const title = document.createElement("h3");
        title.innerText = "Success!";
        popup.appendChild(title);

        const message = document.createElement("p");
        message.innerText = "Data added successfully!";
        popup.appendChild(message);

        const closeButton = document.createElement("button");
        closeButton.innerText = "Close";
        closeButton.classList.add("close-btn");

        // Close button functionality
        closeButton.onclick = () => {
          popup.remove(); // Remove popup
          e.target.reset(); // Clear form fields
        };

        popup.appendChild(closeButton);
        document.body.appendChild(popup);
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      alert("Error while adding data. Please try again.");
      console.error("Add Contact Error:", error);
    }
  });

// Search Contact
document
  .getElementById("searchContactForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const searchQuery = document.getElementById("searchQuery").value;
    const searchType = document.getElementById("searchType").value;

    const query = new URLSearchParams({
      [searchType]: searchQuery,
    });

    try {
      const response = await fetch(`/point-of-contact/?${query}`, {
        method: "GET",
      });

      const result = await response.json();

      if (response.ok && result) {
        // Generate styled output
        const popup = document.createElement("div");
        popup.classList.add("popup");

        const title = document.createElement("h3");
        title.innerText = "Contact Found";
        popup.appendChild(title);

        for (const [key, value] of Object.entries(result)) {
          const field = document.createElement("div");
          field.classList.add("field");

          const label = document.createElement("span");
          label.classList.add("label");
          label.innerText = `${key}: `;

          const fieldValue = document.createElement("span");
          fieldValue.classList.add("value");
          fieldValue.innerText = value;

          field.appendChild(label);
          field.appendChild(fieldValue);
          popup.appendChild(field);
        }

        const closeButton = document.createElement("button");
        closeButton.innerText = "Close";
        closeButton.classList.add("close-btn");
        closeButton.onclick = () => {
          popup.remove();
          document.getElementById("searchContactForm").reset();
        };

        popup.appendChild(closeButton);
        document.body.appendChild(popup);
      } else {
        alert("No contact found with the given criteria.");
      }
    } catch (error) {
      alert("Error while searching data. Please try again.");
      console.error("Search Contact Error:", error);
    }
  });

// Update Contact
document
  .getElementById("updateContactForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const chatUserName = document.getElementById("update_chat_user_name").value;
    const updateField = document.getElementById("updateField").value;
    const updateValue = document.getElementById("updateValue").value;

    try {
      const response = await fetch(`/point-of-contact/${chatUserName}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ [updateField]: updateValue }),
      });

      const result = await response.json();

      if (response.ok) {
        alert("Contact updated successfully!");
        e.target.reset();
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      alert("Error while updating contact.");
    }
  });


// Delete Contact
document
  .getElementById("deleteContactForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const chatUserName = document.getElementById("delete_contact_id").value;

    try {
      const response = await fetch(`/point-of-contact/${chatUserName}`, {
        method: "DELETE",
      });

      const result = await response.json();

      if (response.ok) {
        // Generate styled popup
        const popup = document.createElement("div");
        popup.classList.add("popup");

        const title = document.createElement("h3");
        title.innerText = "Success!";
        popup.appendChild(title);

        const message = document.createElement("p");
        message.innerText = "Contact deleted successfully!";
        popup.appendChild(message);

        const closeButton = document.createElement("button");
        closeButton.innerText = "Close";
        closeButton.classList.add("close-btn");

        // Close button functionality
        closeButton.onclick = () => {
          popup.remove(); // Remove popup
          e.target.reset(); // Clear form field
        };

        popup.appendChild(closeButton);
        document.body.appendChild(popup);
      } else {
        // Handle errors in response
        alert(`Error: ${result.error || "Unable to delete contact"}`);
      }
    } catch (error) {
      alert("Error while deleting data. Please try again.");
      console.error("Delete Contact Error:", error);
    }
  });

