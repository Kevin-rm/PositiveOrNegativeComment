import os
import random

from django.core.exceptions import ValidationError
from django.db import models

from PositiveOrNegativeComment import settings
from base.utils import is_english, translate
from ml.classes import Model

# Create your models here.

model = Model.load(os.path.join(settings.BASE_DIR, "ml", "model.plk"))
replies = {
    1: [
        "Mankasitraka indrindra tompoko oh!",
        "Misaotra betsaka tamin'ny kaomanteranao",
        "Mankasitraka ny hevitrao tompoko!",
        "Tompoko, tena faly izahay nahafinaritra anao! Misaotra indrindra!",
        "Misaotra anao nizara ny zavatra niainanao nahafinaritra anay!",
        "Mankasitraka ny fanohananao! Tena nahafaly anay izany!",
        "Tompoko, faly izahay naheno ny hevitrao tsara. Misaotra indrindra!",
        "Mankasitraka anao noho ny fiaraha-mientana tsara!",
        "Misaotra anao noho ny feedback tsara. Tena mankasitraka izahay!",
        "Ny hevitrao mahafaly anay dia tena zava-dehibe ho anay. Misaotra tompoko!",
        "Tompoko, ny hevitrao dia manentana anay hampitombo hatrany ny kalitao. Misaotra!",
        "Tena faly izahay nahafinaritra anao! Misaotra betsaka!",
        "Ny hafalianao dia ny tanjonay. Misaotra tompoko!",
        "Mankasitraka anao satria ny hevitrao dia manampy anay ho tsara kokoa.",
        "Tompoko, misaotra betsaka tamin'ny hevitrao tsara. Tena ankasitrahanay!"
    ],
    0: [
        "Misaotra anao noho ny hevitrao. Hanatsara izany izahay ary miala tsiny tompoko.",
        "Miala tsiny tompoko, hiezaka izahay ny hanatsara ny kalitao",
        "Tompoko, misaotra anao tamin'ny feedback. Hiezaka hanatsara izahay.",
        "Miala tsiny noho ny tsy fahafaham-ponao. Hiezaka ny hanatsara izahay.",
        "Tompoko, miala tsiny raha tsy araka ny nantenainao. Hanatsara izahay.",
        "Misaotra anao noho ny fanamarihanao. Hiezaka hanatsara ny kalitao izahay.",
        "Tompoko, miala tsiny noho ny olana. Hiezaka ny hanatsara ny traikefan'ny mpanjifa izahay.",
        "Miala tsiny tompoko, hiezaka ny handray an-tsaina ny fanamarihanao izahay.",
        "Misaotra anao tamin'ny feedback. Miala tsiny izahay raha tsy araka ny nantenainao.",
        "Tompoko, miala tsiny noho ny tsy fahatomombanana. Hiezaka izahay hanatsara izany.",
        "Misaotra anao nizara ny olana. Hiezaka izahay ny hanatsara ny zava-misy.",
        "Miala tsiny tompoko, hiezaka hanatsara ny serivisy izahay.",
        "Misaotra tompoko noho ny fanamarihanao. Hiezaka izahay ny hanatsara ny kalitao.",
        "Tompoko, miala tsiny izahay raha nisy olana. Hanatsara ny zavatra izahay.",
        "Misaotra anao noho ny feedback. Hiezaka izahay ny hanatsara ny traikefa."
    ]
}


class Comment(models.Model):
    text = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]

    def clean(self):
        if not self.text.strip():
            raise ValidationError("Banga ny soratra ao amin'ny kaomanteranao")

    def generate_reply(self) -> None:
        global model

        text = self.text
        print(text)
        if not is_english(text):
            text = translate(text)
            print(f"Après translation: {text}")

        prediction = model.predict(text)
        self.reply = random.choice(replies[prediction])
