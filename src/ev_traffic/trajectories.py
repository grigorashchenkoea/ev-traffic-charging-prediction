"""Utilities for processing vehicle trajectories."""


def parse_trajectory(points: str) -> list[tuple[int, float]]:
    """Parse a trajectory string into node IDs and timestamps.

    Consecutive observations of the same node are collapsed into one point.

    Args:
        points: Underscore-separated trajectory points in NodeID-Time format.

    Returns:
        Sequence of unique consecutive (node_id, time) pairs.
    """
    parsed_points = [
        (int(point.split("-")[0]), float(point.split("-")[1]))
        for point in points.split("_")
    ]

    return [
        point
        for index, point in enumerate(parsed_points)
        if index == 0 or point[0] != parsed_points[index - 1][0]
    ]


def extract_movements(
    trajectory: list[tuple[int, float]],
) -> list[tuple[int, int, int, float]]:
    """Extract intersection movements from a parsed trajectory.

    Args:
        trajectory: Sequence of (node_id, time) pairs.

    Returns:
        Sequence of (incoming_node, intersection, outgoing_node, time) movements.
    """
    return [
        (
            trajectory[i - 1][0],
            trajectory[i][0],
            trajectory[i + 1][0],
            trajectory[i][1],
        )
        for i in range(1, len(trajectory) - 1)
    ]
