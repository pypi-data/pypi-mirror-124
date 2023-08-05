# Copyright 2020 Camptocamp (http://www.camptocamp.com).
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

from odoo.addons.base_sparse_field.models.fields import Serialized


class ShopinvaderVariant(models.Model):
    _inherit = "shopinvader.variant"

    packaging = Serialized(
        compute="_compute_packaging",
        help="Technical field to store packaging for the shop",
        store=True,
    )

    @api.depends(lambda self: self._compute_packaging_depends())
    def _compute_packaging(self):
        for rec in self:
            rec.packaging = rec._get_variant_packaging()

    def _compute_packaging_depends(self):
        return (
            "lang_id",
            "record_id.packaging_ids.qty",
            "record_id.packaging_ids.can_be_sold",
            "record_id.packaging_ids.barcode",
            "record_id.packaging_ids.packaging_type_id.name",
        )

    def _get_variant_packaging(self):
        res = []
        ctx = self._get_variant_packaging_ctx()
        rec = self.record_id.with_context(ctx)
        contained_mapping = rec.packaging_contained_mapping or {}
        packaging = rec._ordered_packaging()
        for pkg in packaging:
            pkg_info = self._prepare_qty_by_packaging_values(pkg, pkg.qty)
            pkg_info["contained"] = contained_mapping.get(str(pkg.id))
            res.append(pkg_info)
        return res

    def _get_variant_packaging_ctx(self):
        return {
            "lang": self.lang_id.code,
            # consider only packaging that can be sold
            "_packaging_filter": lambda x: x.can_be_sold,
            "_packaging_values_handler": self._prepare_qty_by_packaging_values,
        }

    def _prepare_qty_by_packaging_values(self, packaging, qty_per_pkg):
        return {
            "id": packaging.id,
            "qty": qty_per_pkg,
            "name": packaging.name,
            "is_unit": packaging.is_unit,
            "barcode": packaging.barcode,
        }
