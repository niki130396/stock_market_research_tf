document.addEventListener("DOMContentLoaded", function() {

    // Function to check if an element is available and execute a callback when it is
    function onElementAvailable(selector, callback) {
        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                observer.disconnect();
                callback();
            }
        });
        observer.observe(document.body, { childList: true, subtree: true });
    }


    const body = document.querySelector("body");

    onElementAvailable(".sidebar", () => {
        const sidebar = document.querySelector(".sidebar")

        sidebar.addEventListener("mouseenter", () => {
          if (sidebar.classList.contains("hoverable")) {
            sidebar.classList.remove("close");
          }
        });

        sidebar.addEventListener("mouseleave", () => {
          if (sidebar.classList.contains("hoverable")) {
            sidebar.classList.add("close");
          }
        });

        if (window.innerWidth < 768) {
          sidebar.classList.add("close");
        } else {
          sidebar.classList.remove("close");
        }

        onElementAvailable(".bottom.expand_sidebar", () => {
            const sidebarExpand = document.querySelector(".bottom.expand_sidebar")

            sidebarExpand.addEventListener("click", () => {
              sidebar.classList.remove("close", "hoverable");
            });
        });

        onElementAvailable(".bottom.collapse_sidebar", () => {
            const sidebarClose = document.querySelector(".bottom.collapse_sidebar")

            sidebarClose.addEventListener("click", () => {
                sidebar.classList.add("close", "hoverable");
            });
        });

        onElementAvailable("#sidebarOpen", () => {
            const sidebarOpen = document.querySelector("#sidebarOpen")

            sidebarOpen.addEventListener("click", () => sidebar.classList.toggle("close"));
        });
    });
    onElementAvailable(".submenu_item", () => {
        const submenuItems = document.querySelector(".submenu_item")

        submenuItems.childNodes.forEach((item, index) => {
          item.addEventListener("click", () => {
            item.classList.toggle("show_submenu");
            submenuItems.childNodes.forEach((item2, index2) => {
              if (index !== index2) {
                item2.classList.remove("show_submenu");
              }
            });
          });
        });
    });


//    sidebarOpen.addEventListener("click", () => sidebar.classList.toggle("close"));
});
