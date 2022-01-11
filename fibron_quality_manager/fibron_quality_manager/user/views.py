# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from fibron_quality_manager.user.models import Job, Spool
from fibron_quality_manager.user.forms import NewJobForm, NewSpoolForm
from fibron_quality_manager.user.tables import JobsTable, SpoolsTable
from fibron_quality_manager.utils import flash_errors


blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")

@blueprint.route("/jobs")
@login_required
def manage_jobs():
    """Manage jobs."""
    # TODO: https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates
    table = JobsTable(Job.query.filter_by().all())
    return render_template("users/jobs.html", table=table)

@blueprint.route("/spools")
@login_required
def manage_spools():
    """Manage spools."""
    table = SpoolsTable(Spool.query.filter_by().all())
    return render_template("users/spools.html", table=table)

@blueprint.route("/add_job", methods=["GET", "POST"])
@login_required
def add_job():
    """Add jobs."""
    form = NewJobForm(request.form)
    if form.validate_on_submit():
        Job.create(
            name=form.name.data,
            creator_user_id=current_user.get_id(),
            product_type=form.product_type.data,
            product_length=form.product_length.data,
            product_diameter=form.product_diameter.data,
            product_layers=form.product_layers.data
        )
        flash("Job has been added sucessfully.", "success")
        return redirect(url_for("user.manage_jobs"))
    else:
        flash_errors(form)
    return render_template("users/add_job.html", form=form)

@blueprint.route("/add_spool", methods=["GET", "POST"])
@login_required
def add_spool():
    """Add spool."""
    form = NewSpoolForm(request.form)
    if form.validate_on_submit():
        Spool.create(
            description=form.description.data,
        )
        flash("New spool has been added.", "success")
        return redirect(url_for("user.manage_spools"))
    else:
        flash_errors(form)
    return render_template("users/add_spool.html", form=form)
