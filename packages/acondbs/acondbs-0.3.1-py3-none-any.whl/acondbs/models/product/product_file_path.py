from ...db.sa import sa


##__________________________________________________________________||
class ProductFilePath(sa.Model):
    __tablename__ = "product_file_paths"
    path_id = sa.Column(sa.Integer(), primary_key=True)
    path = sa.Column(sa.Text())
    note = sa.Column(sa.Text())
    product_id = sa.Column(sa.ForeignKey("products.product_id"))
    product = sa.relationship(
        "Product", backref=sa.backref("paths", cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.path_shorten!r}>"

    @property
    def path_shorten(self):
        try:
            placeholder = "..."
            width = max(20, len(placeholder))
            if len(self.path) <= width:
                return self.path
            return placeholder + self.path[-(width - len(placeholder)) :]
        except BaseException:
            return self.path


##__________________________________________________________________||
