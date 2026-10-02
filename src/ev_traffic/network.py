"""Utilities for analyzing the road network."""

import pandas as pd


def find_highway_exit_candidates(edges: pd.DataFrame) -> set[int]:
    """Identify candidate highway exit decision points.

    A candidate is a node where a motorway or trunk road arrives and the
    vehicle can either continue on the same road class or take the
    corresponding link road.

    Args:
        edges: Directed road edges containing Origin, Destination, and Class.

    Returns:
        Node IDs of candidate highway exit decision points.
    """
    candidates: set[int] = set()

    road_types = {
        "motorway": "motorway_link",
        "trunk": "trunk_link",
    }

    for node in edges["Origin"].unique():
        incoming_classes = set(edges.loc[edges["Destination"] == node, "Class"])
        outgoing_classes = set(edges.loc[edges["Origin"] == node, "Class"])

        for road_class, link_class in road_types.items():
            if (
                road_class in incoming_classes
                and road_class in outgoing_classes
                and link_class in outgoing_classes
            ):
                candidates.add(int(node))

    return candidates


def classify_highway_movement(
    incoming_class: str,
    outgoing_class: str,
    intersection: int,
    exit_candidates: set[int],
) -> str | None:
    """Classify a movement at a highway exit decision point.

    Args:
        incoming_class: Road class used to enter the decision point.
        outgoing_class: Road class used to leave the decision point.
        intersection: Node ID of the decision point.
        exit_candidates: Candidate highway exit decision point node IDs.

    Returns:
        ``"continue"`` if the vehicle remains on the main road,
        ``"exit"`` if it takes the corresponding link road,
        or ``None`` if the movement is not a highway exit decision.
    """
    if intersection not in exit_candidates:
        return None

    if incoming_class == "motorway":
        if outgoing_class == "motorway":
            return "continue"
        if outgoing_class == "motorway_link":
            return "exit"

    if incoming_class == "trunk":
        if outgoing_class == "trunk":
            return "continue"
        if outgoing_class == "trunk_link":
            return "exit"

    return None
