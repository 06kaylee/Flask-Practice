function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }), // turns into a string
    }).then((_res) => {
      window.location.href = "/"; // reloads the home page
    });
  }