from flask import Flask, request, jsonify, render_template
import threading
import json

from client import Client
from globals import var_dict
from flask_caching import Cache


class VarEditorServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.app = Flask(
            __name__,
            template_folder="templates",
            static_folder="static"
        )
        self.cache = Cache(self.app, config={'CACHE_TYPE': 'SimpleCache'})

        self.host = host
        self.port = port

        @self.app.route("/", methods=["GET"])
        def edit_form():
            return render_template("form.html", data=var_dict().getGlobals())

        @self.app.route("/data", methods=["GET"])
        @self.cache.cached(timeout=2)
        def get_data():
            return jsonify(var_dict().getOldGlobals())


        @self.app.route("/submit", methods=["POST"])
        def ajax_submit():
            form_data = request.get_json()
            updated = {}
            errors = []

            for full_key, val in form_data.items():
                if "::" not in full_key:
                    continue
                group, var_name = full_key.split("::", 1)

                if group not in var_dict().getGlobals() or var_name not in var_dict().getGlobals()[group]:
                    continue

                orig_val = var_dict().getGlobals()[group][var_name]
                new_val = self._convert_type(val, type(orig_val))

                if new_val is None:
                    errors.append(f"{group}::{var_name} must be of type {type(orig_val).__name__}")
                    continue

                if group not in updated:
                    updated[group] = {}
                updated[group][var_name] = new_val

            if not errors:
                for group, vars in updated.items():
                    if group not in var_dict().getGlobals():
                        var_dict().getGlobals()[group] = {}
                    for var_name, new_val in vars.items():
                        var_dict().getGlobals()[group][var_name] = new_val
                # var_dict().setGlobals(updated)
                # vars_dict =
                Client().updateServer()
                return jsonify(success=True, data=var_dict().getGlobals())
            else:
                return jsonify(success=False, errors=errors)


    def _convert_type(self, val, target_type):
        try:
            if target_type is bool:
                return val.lower() in ['true', '1', 'yes', 'on']
            return target_type(val)
        except:
            return None

    def run(self):
        threading.Thread(target=lambda: self.app.run(host=self.host, port=self.port, debug=False), daemon=True).start()

    def get_edited_data(self):
        return var_dict().getGlobals()