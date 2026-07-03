import gradio as gr
import json
import urllib.request
import traceback
from shared.utils.plugins import WAN2GPPlugin

MANIFEST_URL = "https://huggingface.co/api/spaces?filter=gradio-theme&limit=1000&sort=likes&direction=-1"

class SkinManagerPlugin(WAN2GPPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Wan2GP Skin Manager"
        self.version = "1.0.0"
        self.description = "Select themes for Gradio from the Gradio Themes Gallery"
        self.themes_data = []
        self.themes_formatted = []
        self._patch_gr_blocks()

    def _patch_gr_blocks(self):
        if hasattr(gr.Blocks, "_wangp_skin_manager_patched"):
            return
        
        original_init = gr.Blocks.__init__
        plugin_instance = self
        
        def patched_init(self_obj, *args, **kwargs):
            if kwargs.get("title") == "WanGP":
                if hasattr(plugin_instance, "server_config") and plugin_instance.server_config:
                    selected_theme = plugin_instance.server_config.get("skin_manager_theme")
                    if selected_theme:
                        kwargs["theme"] = selected_theme
            original_init(self_obj, *args, **kwargs)
            
        gr.Blocks.__init__ = patched_init
        gr.Blocks._wangp_skin_manager_patched = True

    def setup_ui(self):
        self.request_global("server_config")
        self.request_global("server_config_filename")
        self.add_tab("skin_manager", "Skin Manager", self.create_ui)

    def fetch_themes(self):
        try:
            req = urllib.request.Request(MANIFEST_URL)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                self.themes_data = data
                rows = []
                for t in data:
                    theme_id = t.get("id", "")
                    if not theme_id:
                        continue
                    parts = theme_id.split("/")
                    author = parts[0] if len(parts) > 1 else ""
                    name = parts[-1]
                    likes = str(t.get("likes", 0))
                    rows.append([theme_id, author, name, likes])
                self.themes_formatted = rows
                return rows
        except Exception as e:
            traceback.print_exc()
            return []

    def create_ui(self):
        current_theme = ""
        if hasattr(self, "server_config") and self.server_config:
            current_theme = self.server_config.get("skin_manager_theme", "")

        with gr.Column():
            gr.Markdown("## Gradio Themes Gallery")
            gr.Markdown("Select a theme from the gallery to apply it to Wan2GP. (Requires restart to take effect)")
            
            with gr.Row():
                refresh_btn = gr.Button("Fetch / Refresh Themes")
                current_theme_disp = gr.Textbox(label="Currently Selected Theme", value=current_theme, interactive=False)
            
            search_box = gr.Textbox(label="Search Themes", placeholder="Type to filter themes by name or author...")

            themes_grid = gr.Dataframe(
                headers=["ID", "Author", "Name", "Likes"],
                datatype=["str", "str", "str", "str"],
                interactive=False,
                wrap=True,
                type="array"
            )
            
            apply_btn = gr.Button("Apply Selected Theme", variant="primary")
            selected_theme_state = gr.State("")

        def on_refresh():
            return self.fetch_themes()

        def filter_themes(search_text):
            if not search_text:
                return self.themes_formatted
            search_text = search_text.lower()
            return [row for row in self.themes_formatted if search_text in row[1].lower() or search_text in row[2].lower()]
            
        def on_select(evt: gr.SelectData, current_data):
            row = evt.index[0]
            if current_data and row < len(current_data):
                theme_id = current_data[row][0]
                return theme_id, f"Selected: {theme_id}"
            return "", "None selected"

        def apply_theme(theme_id):
            if not theme_id:
                return "Please select a theme first."
            if not getattr(self, "server_config", None):
                return "Error: server_config not found."
            
            self.server_config["skin_manager_theme"] = theme_id
            
            try:
                with open(self.server_config_filename, "w", encoding="utf-8") as f:
                    json.dump(self.server_config, f, indent=4)
                return f"Theme '{theme_id}' applied! Please restart Wan2GP to see changes."
            except Exception as e:
                return f"Error saving config: {e}"

        search_box.change(filter_themes, inputs=[search_box], outputs=[themes_grid])
        refresh_btn.click(on_refresh, inputs=[], outputs=[themes_grid])
        themes_grid.select(on_select, inputs=[themes_grid], outputs=[selected_theme_state, current_theme_disp])
        apply_btn.click(apply_theme, inputs=[selected_theme_state], outputs=[current_theme_disp])
