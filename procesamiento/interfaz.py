import customtkinter as ctk
import cv2
import sys

from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

from PIL import Image
from PIL import ImageTk

import time

from reconocedor.preprocesado import normalize
from reconocedor.detector import identify_img
from reconocedor.detector import set_boxes

from tracking.seguidor import initialize_tracker
from tracking.seguidor import track_frame

from tracking.contador import initialize_counter
from tracking.contador import count_detections
from tracking.contador import counter

class ConsoleRedirect:

    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.insert("end", text)
        self.textbox.see("end")

    def flush(self):
        pass


class Interfaz:

    def __init__(self):

        self.prev_time = time.time()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Contador de Flujo Vehicular")
        self.root.geometry("1200x800")

        self.video_path = ""

        self.cap = None
        self.reproduciendo = False

        self.frame_count = 0

        self.last_result = None
        self.last_resize_info = None

        self.crear_componentes()

    def crear_componentes(self):

        # ========= TÍTULO =========

        titulo = ctk.CTkLabel(
            self.root,
            text="Contador de Flujo Vehicular",
            font=("Arial", 28, "bold")
        )

        titulo.pack(pady=10)

        # ========= SELECTOR VIDEO =========

        frame_selector = ctk.CTkFrame(self.root)
        frame_selector.pack(fill="x", padx=15)

        self.video_entry = ctk.CTkEntry(
            frame_selector,
            width=800
        )

        self.video_entry.pack(
            side="left",
            padx=10,
            pady=10
        )

        btn_examinar = ctk.CTkButton(
            frame_selector,
            text="Examinar",
            command=self.seleccionar_video
        )

        btn_examinar.pack(
            side="left",
            padx=10
        )

        # ========= FRAME PRINCIPAL =========

        frame_principal = ctk.CTkFrame(self.root)

        frame_principal.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # ========= VIDEO =========

        self.video_label = ctk.CTkLabel(
            frame_principal,
            text="Seleccione un video y presione Iniciar"
        )

        self.video_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ========= ESTADÍSTICAS =========

        frame_stats = ctk.CTkFrame(frame_principal)

        frame_stats.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.carros = self.crear_tarjeta(
            frame_stats,
            "Carros",
            "0"
        )

        self.motos = self.crear_tarjeta(
            frame_stats,
            "Motos",
            "0"
        )

        self.buses = self.crear_tarjeta(
            frame_stats,
            "Buses",
            "0"
        )

        self.camiones = self.crear_tarjeta(
            frame_stats,
            "Camiones",
            "0"
        )

        # ========= ESTADO =========

        frame_estado = ctk.CTkFrame(frame_principal)

        frame_estado.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.estado_label = ctk.CTkLabel(
            frame_estado,
            text="Estado: Esperando video"
        )

        self.estado_label.pack(
            anchor="w",
            padx=10
        )

        self.fps_label = ctk.CTkLabel(
            frame_estado,
            text="FPS: 0"
        )

        self.fps_label.pack(
            anchor="w",
            padx=10
        )

        # ========= LOGS =========

        frame_logs = ctk.CTkFrame(frame_principal)

        frame_logs.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            frame_logs,
            text="Registro del Sistema"
        ).pack(anchor="w", padx=10)

        self.log_box = ScrolledText(
            frame_logs,
            height=10,
            bg="#1e1e1e",
            fg="white"
        )

        self.log_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        sys.stdout = ConsoleRedirect(
            self.log_box
        )

        # ========= BOTONES =========

        frame_botones = ctk.CTkFrame(self.root)

        frame_botones.pack(
            fill="x",
            padx=15,
            pady=10
        )

        ctk.CTkButton(
            frame_botones,
            text="Iniciar",
            fg_color="green",
            command=self.iniciar
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame_botones,
            text="Detener",
            fg_color="red",
            command=self.detener
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame_botones,
            text="Salir",
            command=self.root.destroy
        ).pack(side="right", padx=10)

    def crear_tarjeta(self, padre, titulo, valor):

        tarjeta = ctk.CTkFrame(
            padre,
            width=220,
            height=120
        )

        tarjeta.pack(
            side="left",
            expand=True,
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=("Arial", 18)
        ).pack(pady=10)

        valor_label = ctk.CTkLabel(
            tarjeta,
            text=valor,
            font=("Arial", 32, "bold")
        )

        valor_label.pack()

        return valor_label

    def seleccionar_video(self):

        archivo = filedialog.askopenfilename(
            filetypes=[
                ("Videos", "*.mp4 *.avi *.mkv")
            ]
        )

        if archivo:

            self.video_path = archivo

            self.video_entry.delete(0, "end")
            self.video_entry.insert(0, archivo)

            print(f"Video seleccionado: {archivo}")

    def iniciar(self):

        if not self.video_path:
            print("Seleccione un video primero")
            return

        self.cap = cv2.VideoCapture(
            self.video_path
        )

        if not self.cap.isOpened():
            print("No se pudo abrir el video")
            return

        self.reproduciendo = True

        initialize_tracker()

        initialize_counter(
            (
                "car",
                "motorcycle",
                "bus",
                "truck"
            ),
            (300, 300),
            (900, 300),
            (300, 400),
            (900, 400)
        )

        self.video_fps = self.cap.get(
            cv2.CAP_PROP_FPS
        )

        if self.video_fps <= 0:
            self.video_fps = 30

        self.estado_label.configure(
            text="Estado: Procesando"
        )

        print("Video abierto correctamente")

        self.actualizar_video()

    def actualizar_video(self):

        if not self.reproduciendo:
            return

        ret, frame = self.cap.read()

        if not ret:

            self.cap.release()

            self.reproduciendo = False

            self.estado_label.configure(
                text="Estado: Finalizado"
            )

            print("Fin del video")

            return


        self.frame_count += 1

        if self.frame_count % 3 == 0:

            normalized_img, resize_info = normalize(frame)

            result = identify_img(
                normalized_img,
                filter_threshold=0.5
            )

            detections, names = track_frame(result)

            count_detections(detections, names)

            self.actualizar_contadores(
                counter.get("car", 0),
                counter.get("motorcycle", 0),
                counter.get("bus", 0),
                counter.get("truck", 0)
            )

            self.last_result = result
            self.last_resize_info = resize_info

        if self.last_result is not None:

            frame = set_boxes(
                frame,
                self.last_result,
                self.last_resize_info
            )

        current_time = time.time()

        fps = 1 / (current_time - self.prev_time)

        self.prev_time = current_time

        self.fps_label.configure(
            text=f"FPS: {fps:.1f}"
        )

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        imagen = Image.fromarray(frame_rgb)

        imagen.thumbnail((900, 500))

        foto = ImageTk.PhotoImage(imagen)

        self.video_label.configure(
            image=foto,
            text=""
        )

        self.video_label.image = foto

        delay = int(1000 / self.video_fps)

        self.root.after(
            delay,
            self.actualizar_video
        )

    def detener(self):

        self.reproduciendo = False

        if self.cap:
            self.cap.release()

        self.estado_label.configure(
            text="Estado: Detenido"
        )

        print("Procesamiento detenido")

    def actualizar_contadores(
        self,
        carros,
        motos,
        buses,
        camiones
    ):

        self.carros.configure(
            text=str(carros)
        )

        self.motos.configure(
            text=str(motos)
        )

        self.buses.configure(
            text=str(buses)
        )

        self.camiones.configure(
            text=str(camiones)
        )

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":

    app = Interfaz()
    app.ejecutar()