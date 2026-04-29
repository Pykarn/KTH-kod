class Dator:
    def __init__(self, märke, processor):
        self.märke = märke
        self.processor = processor

    def __str__(self):
        return self.märke+" "+self.processor






min_laptop = Dator("Dell", "quad-core")
print(min_laptop)
