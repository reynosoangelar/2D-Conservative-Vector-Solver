import streamlit as st
import sympy as sp

# Create the mathematical variables
x, y = sp.symbols("x y")


# Convert what the user types into a SymPy expression
def convert_input(user_input):
    user_input = user_input.replace("^", "**")

    return sp.sympify(
        user_input,
        locals={
            "x": x,
            "y": y,
            "sin": sp.sin,
            "cos": sp.cos,
            "exp": sp.exp,
            "sqrt": sp.sqrt,
            "ln": sp.log,
            "pi": sp.pi,
        },
    )


# Set up the webpage
st.title("2D Line Integral Solver")

st.caption("Created by Angel Reynoso")

st.write(
    "This program checks whether a vector field is conservative, "
    "finds the potential function, and applies the Fundamental "
    "Theorem of Line Integrals."
)

st.write(
    r"Enter the vector field "
    r"$\mathbf{F}(x,y)=\langle P(x,y),Q(x,y)\rangle$."
)

st.info("Use * for multiplication. Example: 2*x*y")


# Get P and Q from the user
P_input = st.text_input(
    "Enter P(x,y):",
    "2*x*y + 3",
)

Q_input = st.text_input(
    "Enter Q(x,y):",
    "x^2 + 4*y",
)


# Get the starting point
st.subheader("Starting Point A")

start_col1, start_col2 = st.columns(2)

with start_col1:
    x1_input = st.text_input("Starting x-value:", "0")

with start_col2:
    y1_input = st.text_input("Starting y-value:", "0")


# Get the ending point
st.subheader("Ending Point B")

end_col1, end_col2 = st.columns(2)

with end_col1:
    x2_input = st.text_input("Ending x-value:", "1")

with end_col2:
    y2_input = st.text_input("Ending y-value:", "1")


# Run the program when the user clicks Solve
if st.button("Solve"):

    try:
        # Convert all inputs into mathematical expressions
        P = convert_input(P_input)
        Q = convert_input(Q_input)

        x1 = convert_input(x1_input)
        y1 = convert_input(y1_input)

        x2 = convert_input(x2_input)
        y2 = convert_input(y2_input)

        # -------------------------------------------------
        # STEP 1: Display the vector field
        # -------------------------------------------------

        st.header("Step 1: Vector Field")

        st.latex(
            rf"\mathbf{{F}}(x,y)"
            rf"="
            rf"\left\langle"
            rf"{sp.latex(P)},"
            rf"{sp.latex(Q)}"
            rf"\right\rangle"
        )

        # -------------------------------------------------
        # STEP 2: Cross-partial check
        # -------------------------------------------------

        st.header("Step 2: Cross-Partial Check")

        P_y = sp.diff(P, y)
        Q_x = sp.diff(Q, x)

        st.write("Differentiate P with respect to y:")

        st.latex(
            rf"\frac{{\partial P}}{{\partial y}}"
            rf"="
            rf"{sp.latex(P_y)}"
        )

        st.write("Differentiate Q with respect to x:")

        st.latex(
            rf"\frac{{\partial Q}}{{\partial x}}"
            rf"="
            rf"{sp.latex(Q_x)}"
        )

        # Check whether the cross partials are equal
        if sp.simplify(P_y - Q_x) != 0:

            st.error(
                "The cross partial derivatives are not equal."
            )

            st.write(
                "Therefore, the vector field is not conservative."
            )

            st.write(
                "The Fundamental Theorem of Line Integrals "
                "cannot be used."
            )

        else:

            st.success(
                "The cross partial derivatives are equal."
            )

            st.write(
                "Assuming the domain is simply connected, "
                "the vector field is conservative."
            )

            # -------------------------------------------------
            # STEP 3: Find the potential function
            # -------------------------------------------------

            st.header("Step 3: Find the Potential Function")

            st.write("Integrate P with respect to x:")

            first_part = sp.integrate(P, x)

            st.latex(
                rf"f(x,y)"
                rf"="
                rf"\int {sp.latex(P)}\,dx"
            )

            st.latex(
                rf"f(x,y)"
                rf"="
                rf"{sp.latex(first_part)}+g(y)"
            )

            st.write(
                "Differentiate this result with respect to y:"
            )

            first_part_y = sp.diff(first_part, y)

            st.latex(
                rf"f_y"
                rf"="
                rf"{sp.latex(first_part_y)}+g'(y)"
            )

            st.write("Set this equal to Q and solve for g'(y):")

            g_prime = sp.simplify(Q - first_part_y)

            st.latex(
                rf"g'(y)"
                rf"="
                rf"{sp.latex(g_prime)}"
            )

            st.write("Integrate g'(y) with respect to y:")

            g = sp.integrate(g_prime, y)

            st.latex(
                rf"g(y)"
                rf"="
                rf"{sp.latex(g)}"
            )

            # Combine both parts
            potential = sp.simplify(first_part + g)

            st.success("Potential function found:")

            st.latex(
                rf"f(x,y)"
                rf"="
                rf"{sp.latex(potential)}+C"
            )

            # -------------------------------------------------
            # STEP 4: Verify the potential function
            # -------------------------------------------------

            st.header("Step 4: Verify the Potential Function")

            potential_x = sp.diff(potential, x)
            potential_y = sp.diff(potential, y)

            st.latex(
                rf"f_x"
                rf"="
                rf"{sp.latex(potential_x)}"
            )

            st.latex(
                rf"f_y"
                rf"="
                rf"{sp.latex(potential_y)}"
            )

            if (
                sp.simplify(potential_x - P) == 0
                and sp.simplify(potential_y - Q) == 0
            ):

                st.success(
                    "The derivatives match the original vector field."
                )

            else:

                st.error(
                    "The potential function could not be verified."
                )

                st.stop()

            # -------------------------------------------------
            # STEP 5: Fundamental Theorem
            # -------------------------------------------------

            st.header(
                "Step 5: Fundamental Theorem of Line Integrals"
            )

            st.latex(
                rf"\int_C \mathbf{{F}}\cdot d\mathbf{{r}}"
                rf"="
                rf"f(B)-f(A)"
            )

            # Evaluate the potential function at point A
            f_A = potential.subs(
                {
                    x: x1,
                    y: y1,
                }
            )

            # Evaluate the potential function at point B
            f_B = potential.subs(
                {
                    x: x2,
                    y: y2,
                }
            )

            st.write("Evaluate the ending point:")

            st.latex(
                rf"f({sp.latex(x2)},{sp.latex(y2)})"
                rf"="
                rf"{sp.latex(f_B)}"
            )

            st.write("Evaluate the starting point:")

            st.latex(
                rf"f({sp.latex(x1)},{sp.latex(y1)})"
                rf"="
                rf"{sp.latex(f_A)}"
            )

            # Subtract f(A) from f(B)
            answer = sp.simplify(f_B - f_A)

            st.write("Subtract:")

            st.latex(
                rf"f(B)-f(A)"
                rf"="
                rf"{sp.latex(f_B)}"
                rf"-"
                rf"\left({sp.latex(f_A)}\right)"
            )

            st.success("Final Answer")

            st.latex(
                rf"\boxed{{"
                rf"\int_C \mathbf{{F}}\cdot d\mathbf{{r}}"
                rf"="
                rf"{sp.latex(answer)}"
                rf"}}"
            )

    except Exception as error:

        st.error("There is a problem with the input.")

        st.write(
            "Remember to use * for multiplication."
        )

        st.write(
            "For example, enter 2*x*y instead of 2xy."
        )

        st.write("Error details:", error)

        st.divider()