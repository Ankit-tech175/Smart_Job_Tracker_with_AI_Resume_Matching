import os

from flask import (
    Blueprint,
    request,
    current_app
)

from werkzeug.utils import secure_filename

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from backend.database.extensions import db

from backend.models.job_model import JobApplication
from backend.models.user_model import User

from backend.utils.file_handler import allowed_file

from backend.utils.response import (
    success_response,
    error_response
)

from nlp.parser import parse_resume

from nlp.matcher import (
    calculate_ats_score,
    extract_job_skills,
    analyze_skill_gap,
    generate_resume_suggestions
)


job_bp = Blueprint(
    "jobs",
    __name__
)


# =========================
# ADD JOB APPLICATION
# =========================
@job_bp.route("/add", methods=["POST"])
@jwt_required()
def add_job():

    try:

        # Get logged-in user ID
        current_user_id = get_jwt_identity()

        # Find current user
        user = User.query.get(
            current_user_id
        )

        if not user:

            return error_response(
                "User not found",
                404
            )

        data = request.get_json()

        company_name = data.get(
            "company_name"
        )

        job_title = data.get(
            "job_title"
        )

        job_link = data.get(
            "job_link"
        )

        status = data.get(
            "status"
        )

        notes = data.get(
            "notes"
        )

        # Validate required fields
        if not company_name or not job_title:

            return error_response(
                "Company name and job title are required",
                400
            )

        # Create new job application
        new_job = JobApplication(
            company_name=company_name,
            job_title=job_title,
            job_link=job_link,
            status=status if status else "Applied",
            notes=notes,
            user_id=user.id
        )

        # Save to database
        db.session.add(new_job)

        db.session.commit()

        return success_response(
            "Job application added successfully",
            data={
                "job_id": new_job.id,
                "company_name": new_job.company_name,
                "job_title": new_job.job_title,
                "status": new_job.status
            },
            status_code=201
        )

    except Exception as e:

        return error_response(
            str(e),
            500
        )


# =========================
# GET USER JOB APPLICATIONS
# =========================
@job_bp.route("/my-jobs", methods=["GET"])
@jwt_required()
def get_user_jobs():

    try:

        # Get logged-in user ID
        current_user_id = get_jwt_identity()

        # Fetch user jobs
        jobs = JobApplication.query.filter_by(
            user_id=current_user_id
        ).order_by(
            JobApplication.created_at.desc()
        ).all()

        jobs_data = []

        for job in jobs:

            jobs_data.append({

                "id": job.id,

                "company_name":
                    job.company_name,

                "job_title":
                    job.job_title,

                "job_link":
                    job.job_link,

                "status":
                    job.status,

                "notes":
                    job.notes,

                "created_at":
                    job.created_at.strftime(
                        "%d-%m-%Y %H:%M"
                    )
            })

        return success_response(
            "Jobs fetched successfully",
            data=jobs_data,
            status_code=200
        )

    except Exception as e:

        return error_response(
            str(e),
            500
        )


# =========================
# UPDATE JOB STATUS
# =========================
@job_bp.route(
    "/update-status/<int:job_id>",
    methods=["PUT"]
)
@jwt_required()
def update_job_status(job_id):

    try:

        current_user_id = get_jwt_identity()

        # Find user job
        job = JobApplication.query.filter_by(
            id=job_id,
            user_id=current_user_id
        ).first()

        if not job:

            return error_response(
                "Job application not found",
                404
            )

        data = request.get_json()

        new_status = data.get("status")

        # Validate status
        if not new_status:

            return error_response(
                "Status is required",
                400
            )

        # Update job status
        job.status = new_status

        db.session.commit()

        return success_response(
            "Job status updated successfully",
            data={
                "job_id": job.id,
                "updated_status": job.status
            },
            status_code=200
        )

    except Exception as e:

        return error_response(
            str(e),
            500
        )


# =========================
# DELETE JOB APPLICATION
# =========================
@job_bp.route(
    "/delete/<int:job_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_job(job_id):

    try:

        current_user_id = get_jwt_identity()

        # Find user job
        job = JobApplication.query.filter_by(
            id=job_id,
            user_id=current_user_id
        ).first()

        if not job:

            return error_response(
                "Job application not found",
                404
            )

        # Delete job
        db.session.delete(job)

        db.session.commit()

        return success_response(
            "Job application deleted successfully",
            status_code=200
        )

    except Exception as e:

        return error_response(
            str(e),
            500
        )


# =========================
# JOB APPLICATION ANALYTICS
# =========================
@job_bp.route("/analytics", methods=["GET"])
@jwt_required()
def job_analytics():

    try:

        current_user_id = get_jwt_identity()

        # Fetch all jobs
        jobs = JobApplication.query.filter_by(
            user_id=current_user_id
        ).all()

        # Analytics
        total_applications = len(jobs)

        interview_count = len([
            job for job in jobs
            if job.status == "Interview"
        ])

        rejected_count = len([
            job for job in jobs
            if job.status == "Rejected"
        ])

        offer_count = len([
            job for job in jobs
            if job.status == "Offer"
        ])

        applied_count = len([
            job for job in jobs
            if job.status == "Applied"
        ])

        return success_response(
            "Analytics fetched successfully",
            data={
                "total_applications":
                    total_applications,

                "applied_count":
                    applied_count,

                "interview_count":
                    interview_count,

                "rejected_count":
                    rejected_count,

                "offer_count":
                    offer_count
            },
            status_code=200
        )

    except Exception as e:

        return error_response(
            str(e),
            500
        )


# =========================
# UPLOAD RESUME
# =========================
@job_bp.route(
    "/upload-resume",
    methods=["POST"]
)
@jwt_required()
def upload_resume():

    try:

        # Check file exists
        if "resume" not in request.files:

            return error_response(
                "Resume file is required",
                400
            )

        file = request.files["resume"]

        # Validate filename
        if file.filename == "":

            return error_response(
                "No file selected",
                400
            )

        # Validate file extension
        if not allowed_file(
            file.filename,
            current_app.config[
                "ALLOWED_EXTENSIONS"
            ]
        ):

            return error_response(
                "Only PDF, DOC, DOCX files are allowed",
                400
            )

        # Secure filename
        filename = secure_filename(
            file.filename
        )

        # Create upload path
        upload_path = os.path.join(
            current_app.config[
                "UPLOAD_FOLDER"
            ],
            filename
        )

        # Save file
        file.save(upload_path)

        return success_response(
            "Resume uploaded successfully",
            data={
                "filename": filename
            },
            status_code=201
        )

    except Exception as e:

        return error_response(
            str(e),
            500
        )


# =========================
# AI RESUME ANALYZER
# =========================
@job_bp.route(
    "/analyze-resume",
    methods=["POST"]
)
@jwt_required()
def analyze_resume():

    try:

        # Validate uploaded file
        if "resume" not in request.files:

            return error_response(
                "Resume file is required",
                400
            )

        file = request.files["resume"]

        if file.filename == "":

            return error_response(
                "No file selected",
                400
            )

        # Validate file extension
        if not allowed_file(
            file.filename,
            current_app.config[
                "ALLOWED_EXTENSIONS"
            ]
        ):

            return error_response(
                "Only PDF, DOC, DOCX files are allowed",
                400
            )

        # Get job description
        job_description = request.form.get(
            "job_description"
        )

        if not job_description:

            return error_response(
                "Job description is required",
                400
            )

        # Secure filename
        filename = secure_filename(
            file.filename
        )

        # Create upload path
        upload_path = os.path.join(
            current_app.config[
                "UPLOAD_FOLDER"
            ],
            filename
        )

        # Save resume
        file.save(upload_path)

        # Parse resume
        parsed_resume = parse_resume(
            upload_path
        )

        resume_text = parsed_resume[
            "resume_text"
        ]

        resume_skills = parsed_resume[
            "skills"
        ]

        # Extract job description skills
        job_skills = extract_job_skills(
            job_description
        )

       # Calculate ATS score
       # using extracted skills
        ats_score = calculate_ats_score(
       resume_skills,
       job_skills
    )

        # Analyze missing skills
        skill_analysis = analyze_skill_gap(
            resume_skills,
            job_skills
        )
        # Generate AI suggestions
        recommendations = generate_resume_suggestions(
        skill_analysis["missing_skills"],
         ats_score
       )
        
        return success_response(
            "Resume analyzed successfully",
            data={

                # ATS Score
                "ats_score":
                    ats_score,

                # Resume Skills
                "resume_skills":
                    resume_skills,

                # Job Description Skills
                "job_skills":
                    job_skills,

                # Matched Skills
                "matched_skills":
                    skill_analysis[
                        "matched_skills"
                    ],

                # Missing Skills
"missing_skills":
    skill_analysis[
        "missing_skills"
    ],

# AI Recommendations
"recommendations":
    recommendations
            },
            status_code=200
        )

    except Exception as e:

        return error_response(
            str(e),
            500
        )