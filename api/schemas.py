from apiflask import Schema, fields, validators


class BaseSchema(Schema):
    class Meta:
        strict = True
        ordered = True


class SubmitUrlInput(BaseSchema):
    shortcode = fields.String(
        required=False,
        validate=[
            validators.Length(min=4),
            validators.Regexp(
                r"^[0-9a-zA-Z]+$",
                error="Shortcode must be composed of alphanumeric characters only.",
            ),
        ],
        metadata={
            "description": (
                "A short string that can be used to retrieve the supplied URL in the"
                " future. Will be automatically generated if not supplied. Must be at"
                " least 4 characters long and composed of alphanumeric characters."
            )
        },
    )
    url = fields.String(
        required=True,
        validate=validators.URL(),
        metadata={"description": "The URL to be shortened."},
    )


class UrlStatsOutput(BaseSchema):
    shortcode = fields.String(
        required=True,
        metadata={
            "description": "A short string that can be used to retrieve the URL."
        },
    )
    url = fields.String(
        required=True,
        metadata={
            "description": (
                "The URL that the user will be redirected to when querying the"
                " shortened URL."
            )
        },
    )
    created_at = fields.DateTime(
        required=True,
        as_string=True,
        metadata={
            "description": (
                "The time at which this URL was registered with this service."
            )
        },
    )
    accessed_at = fields.DateTime(
        required=True,
        as_string=True,
        metadata={
            "description": (
                "The time at which this URL was last accessed using this service."
            )
        },
    )
    access_count = fields.Integer(
        required=True,
        metadata={
            "description": (
                "The number of times that this URL has been accessed using this"
                " service."
            )
        },
    )
